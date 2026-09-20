import math
from enum import Enum
from typing import override, TYPE_CHECKING
from itertools import permutations

from ..components import Battery, CarBattery, ExternalGrid
from ._base import ActionResult, IAction

if TYPE_CHECKING:
    from .. import IMicrogrid


class EnergySource(Enum):
    """Lists possible energy sources for buying or using stored energy in case of an energy deficiency."""

    EXTERNAL_GRID = ExternalGrid
    BATTERY = Battery
    CAR_BATTERY = CarBattery

    @classmethod
    def priority_order(cls, *sources: "EnergySource") -> tuple["EnergySource"]:
        """Returns the energy sources in the given priority order."""
        return tuple(sources)


class EnergyDeficiencyAction(IAction):
    """Given an energy deficiency (our DER can't meet our energy requirements),
    this action takes the energy source priority order and uses the energy source given first.
    If it can't meet the required energy, the next energy source will be used.

    Attributes:
        energy_source_priority (tuple[EnergySource]): Priority order of energy sources to use. Must include each EnergySource exactly once.
    """

    def __init__(
        self,
        possible_energy_sources: tuple[EnergySource],
        energy_source_priority: tuple[EnergySource],
    ):
        super().__init__()
        if set(possible_energy_sources) != set(energy_source_priority):
            raise ValueError("The priority tuple[] must include each EnergySource exactly once.")
        self.possible_energy_sources: tuple[EnergySource] = possible_energy_sources
        self.energy_source_priority: tuple[EnergySource] = energy_source_priority
        self.missing_energy = None

    def set_missing_energy(self, missing_energy: float):
        self.missing_energy = missing_energy

    @override
    def execute(self, microgrid: "IMicrogrid", time_step: int) -> ActionResult:
        """Executes energy compensation using prioritized energy sources."""

        if self.missing_energy is None:
            raise ValueError("missing_energy not set. Call set_missing_energy() before execute().")

        remaining_energy = self.missing_energy

        for source in self.energy_source_priority:
            if remaining_energy <= 0:
                break

            if source == EnergySource.BATTERY:
                discharged = microgrid.battery.discharge(remaining_energy)
                remaining_energy -= discharged

            elif source == EnergySource.CAR_BATTERY:
                discharged = microgrid.car_battery.discharge(remaining_energy)
                remaining_energy -= discharged

            elif source == EnergySource.EXTERNAL_GRID:
                # Will handle below to also calculate price
                break

        # What remains must come from external grid
        energy_bought = max(0, remaining_energy)
        price = microgrid.external_grid.buy(energy_bought)

        return ActionResult(energy_bought=energy_bought, energy_sold=0, price=price)

    @classmethod
    @override
    def calc_action_space(cls, possible_sources: list[EnergySource]) -> int:
        """Calculates the needed action space.

        Returns:
            The number of possible permutations for the energy_feed_priority List ``n!``
        """
        return math.factorial(len(possible_sources))

    @classmethod
    @override
    def from_action_space(cls, action: int, **kwargs) -> "EnergyDeficiencyAction":
        possible_sources: list[EnergySource] = kwargs["possible_sources"]

        if action < 0 or action >= cls.calc_action_space(possible_sources):
            raise ValueError(f"Action ({action}) has to be in range [0, {cls.calc_action_space(possible_sources)})")

        possible_source_priorities = list(permutations(possible_sources, len(possible_sources)))
        source_priorities = possible_source_priorities[action]
        return cls(possible_sources, source_priorities)

    @override
    def to_action_space(self) -> int:
        return list(permutations(self.possible_energy_sources, len(self.possible_energy_sources))).index(
            self.energy_source_priority
        )

    def __repr__(self):
        return f"EnergyDeficiencyAction({self.energy_source_priority})"
