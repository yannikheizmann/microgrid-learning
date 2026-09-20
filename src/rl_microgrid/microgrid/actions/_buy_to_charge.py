from ._base import ActionResult, IAction
from enum import Enum
from typing import override
from ..components import Battery, CarBattery
from itertools import permutations
import math


class ChargeAmount(Enum):
    NONE = 0
    MINIMAL = 0.1
    QUARTER = 0.25
    HALF = 0.5


class BatteryType(Enum):
    BATTERY = Battery
    CAR_BATTERY = CarBattery

    @classmethod
    def priority_order(cls, *sources: "BatteryType") -> tuple["BatteryType"]:
        """Returns the energy sources in the given priority order."""
        return tuple(sources)


class BuyToChargeAction(IAction):
    def __init__(self, amount, battery_priority):
        super().__init__()
        self.amount: ChargeAmount = amount
        self.battery_priority: tuple[BatteryType] = battery_priority

    @classmethod
    @override
    def calc_action_space(cls):
        return len(ChargeAmount) * math.factorial(len(BatteryType))

    @override
    def execute(self, microgrid, time_step):
        remaining_energy = self.amount.value * microgrid.battery._capacity
        energy_bought = remaining_energy
        for battery in self.battery_priority:
            if remaining_energy <= 0:
                break
            if battery == BatteryType.CAR_BATTERY:
                remaining_energy = microgrid.car_battery.charge(remaining_energy)
            elif battery == BatteryType.BATTERY:
                remaining_energy = microgrid.battery.charge(remaining_energy)
        energy_sold = max(0, remaining_energy)
        price = microgrid.external_grid.sell(energy_sold) - microgrid.external_grid.buy(energy_bought)

        return ActionResult(energy_bought=energy_bought, energy_sold=energy_sold, price=price)

    @classmethod
    @override
    def from_action_space(cls, action: int, **kwargs):
        if action < 0 or action >= cls.calc_action_space():
            raise ValueError(f"Action ({action}) has to be in range [0, {cls.calc_action_space()})")
        chargeAmounts = list(ChargeAmount)
        possible_destination_priorities = list(permutations(BatteryType, len(BatteryType)))
        priority_idx = action // len(chargeAmounts)
        amount_idx = action % len(chargeAmounts)
        battery_priority = possible_destination_priorities[priority_idx]
        amount = chargeAmounts[amount_idx]
        return cls(battery_priority=battery_priority, amount=amount)

    def to_action_space(self) -> int:
        # TODO get action (int) from instance attributes
        # Inverse of from_action_space
        pass
