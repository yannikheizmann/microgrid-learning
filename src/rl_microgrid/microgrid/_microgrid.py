import random

import numpy as np

from ._base import IMicrogrid
from .actions import CompositeBasicAction, CompositeCarAction
from .components import (
    Battery,
    ExternalGrid,
    ResidentialLoad,
    DistributedEnergyResources,
    CarBattery,
)


class BasicMicrogrid(IMicrogrid):
    battery: Battery
    external_grid: ExternalGrid
    residential_loads: list[ResidentialLoad]
    distributed_energy_resources: DistributedEnergyResources

    def __init__(
        self,
        battery: Battery,
        external_grid: ExternalGrid,
        residential_loads: list[ResidentialLoad],
        distributed_energy_resources: DistributedEnergyResources,
    ):
        super().__init__(action_type=CompositeBasicAction)
        self.battery = battery
        self.external_grid = external_grid
        self.residential_loads = residential_loads
        self.distributed_energy_resources = distributed_energy_resources

    @classmethod
    def calc_observation_space(cls) -> tuple[int]:
        # TODO (could be instance method)
        return (7,)

    def vectorize(self, day, iteration, time_step: int) -> np.ndarray:
        """Returns a Numpy-array filled with the attributes of the class"""
        values = [
            self.battery.SoC,
            self.external_grid.get_buy_price(time_step),
            self.external_grid.get_sell_price(time_step),
            time_step,
            self.distributed_energy_resources.getCurrentGeneration(day, iteration, time_step),
        ]
        values.extend(load.get_normalized_load() for load in self.residential_loads)
        return np.array(values, dtype=np.float32)

    def before_step(self, day: int, iterations: int, time_step: int) -> None:
        self.external_grid.set_time(day * iterations + time_step)

    def reset(self) -> None:
        pass

    def info(self, day: int, iterations: int, time_step: int) -> dict:
        return {
            "loads": [load.load() for load in self.residential_loads],
            "battery_percent": self.battery.SoC,
            "battery_kWh": self.battery.SoC_kWh,
            "energy_generated": self.distributed_energy_resources.current_generation(day * iterations + time_step - 1),
            "grid_buy_price": self.external_grid.get_buy_price(day * iterations + time_step - 1),
            "grid_sell_price": self.external_grid.get_sell_price(day * iterations + time_step - 1),
        }


class CarBatteryMicrogrid(IMicrogrid):
    battery: Battery
    car_battery: CarBattery
    external_grid: ExternalGrid
    residential_loads: list[ResidentialLoad]
    distributed_energy_resources: DistributedEnergyResources

    def __init__(
        self,
        battery: Battery,
        car_battery: CarBattery,
        external_grid: ExternalGrid,
        residential_loads: list[ResidentialLoad],
        distributed_energy_resources: DistributedEnergyResources,
    ):
        super().__init__(action_type=CompositeCarAction)
        self.battery = battery
        self.car_battery = car_battery
        self.external_grid = external_grid
        self.residential_loads = residential_loads
        self.distributed_energy_resources = distributed_energy_resources

    @classmethod
    def calc_observation_space(cls) -> tuple[int]:
        # TODO (could be instance method)
        return (10,)

    def vectorize(self, day, iteration, time_step: int) -> np.ndarray:
        """Returns a Numpy-array filled with the attributes of the class"""
        values = [
            self.battery.SoC,
            self.external_grid.get_buy_price(time_step),
            self.external_grid.get_sell_price(time_step),
            time_step,
            self.distributed_energy_resources.getCurrentGeneration(day, iteration, time_step),
            self.car_battery.SoC,
            self.car_battery.desired_soc,
            self.car_battery.target_time,
            int(self.car_battery.can_be_charged),
        ]
        values.extend(load.get_normalized_load() for load in self.residential_loads)
        return np.array(values, dtype=np.float32)

    def before_step(self, day: int, iterations: int, time_step: int) -> None:
        self.external_grid.set_time(day * iterations + time_step)

    def reset(self):
        self.car_battery.setTargetTime(random.randint(6, 13))
        self.car_battery.setDesiredSoc(random.random())

    def info(self, day: int, iterations: int, time_step: int) -> dict:
        return {
            "loads": [load.load() for load in self.residential_loads],
            "battery_percent": self.battery.SoC,
            "battery_kWh": self.battery.SoC_kWh,
            "carbattery_kWh": self.car_battery.SoC_kWh,
            "energy_generated": self.distributed_energy_resources.current_generation(day * iterations + time_step - 1),
            "grid_buy_price": self.external_grid.get_buy_price(day * iterations + time_step - 1),
            "grid_sell_price": self.external_grid.get_sell_price(day * iterations + time_step - 1),
        }
