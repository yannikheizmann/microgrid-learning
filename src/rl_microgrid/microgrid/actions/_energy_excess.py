import math
from enum import Enum
from itertools import permutations
from typing import override, TYPE_CHECKING

from ..components import Battery, ExternalGrid, CarBattery
from ._base import ActionResult, IAction

if TYPE_CHECKING:
    from .. import IMicrogrid


class EnergyFeed(Enum):
    """
    Lists all possible energy feeds for saving or selling excess energy.
    """

    EXTERNAL_GRID = ExternalGrid
    BATTERY = Battery
    CAR_BATTERY = CarBattery

    @classmethod
    def priority_order(cls, *sources: "EnergyFeed") -> tuple["EnergyFeed"]:
        """Returns the energy sources in the given priority order."""
        return tuple(sources)


class EnergyExcessAction(IAction):
    """Given an energy excess (our DER produces more energy than we need),
    this action takes the energy feed priority order and uses the energy feed given first.
    If it cannot store all the available energy, the next energy feed will be used.

    Attributes:
        energy_feed_priority (tuple[EnergyFeed]): Priority order of energy feeds to use. Must include each EnergyFeed exactly once.
    """

    def __init__(
        self,
        possible_energy_feeds: tuple[EnergyFeed],
        energy_feed_priority: tuple[EnergyFeed],
    ):
        super().__init__()
        if set(possible_energy_feeds) != set(energy_feed_priority):
            raise ValueError(
                f"The priority tuple must include each possible EnergyFeed exactly once. {possible_energy_feeds} <> {energy_feed_priority}"
            )
        self.possible_energy_feeds: tuple[EnergyFeed] = possible_energy_feeds
        self.energy_feed_priority: tuple[EnergyFeed] = energy_feed_priority
        self.available_energy = None

    def set_available_energy(self, available_energy: float):
        self.available_energy = available_energy

    @override
    def execute(self, microgrid: "IMicrogrid", time_step: int) -> ActionResult:
        """Distributes available energy across prioritized energy sinks.

        Args:
            microgrid: environment to manipulate
            time_step: current time step in hours

        Returns:
            How much energy was sold to the grid and the price at which it was sold, wrapped in an ActionResult.
        """
        if self.available_energy is None:
            raise ValueError("available_energy not set. Call set_available_energy() before execute().")

        remaining_energy = self.available_energy

        for source in self.energy_feed_priority:
            if remaining_energy <= 0:
                break

            if source == EnergyFeed.BATTERY:
                remaining_energy = microgrid.battery.charge(remaining_energy)

            elif source == EnergyFeed.CAR_BATTERY:
                remaining_energy = microgrid.car_battery.charge(remaining_energy)

            elif source == EnergyFeed.EXTERNAL_GRID:
                # Remaining energy will be sold to grid below
                break

        energy_sold = max(0, remaining_energy)
        price = microgrid.external_grid.sell(energy_sold)

        return ActionResult(energy_bought=0, energy_sold=energy_sold, price=price)

    @classmethod
    @override
    def calc_action_space(cls, possible_feeds: list[EnergyFeed]) -> int:
        """Calculates the necessary action space.

        Returns:
            The number of possible permutations for the energy_feed_priority List ``n!``
        """
        return math.factorial(len(possible_feeds))

    @classmethod
    @override
    def from_action_space(cls, action: int, **kwargs) -> "EnergyExcessAction":
        possible_feeds: list[EnergyFeed] = kwargs["possible_feeds"]

        if action < 0 or action >= cls.calc_action_space(possible_feeds):
            raise ValueError(f"Action ({action}) has to be in range [0, {cls.calc_action_space(possible_feeds)})")

        possible_feed_priorities = list(permutations(possible_feeds, len(possible_feeds)))
        feed_priorities = possible_feed_priorities[action]
        return cls(possible_feeds, feed_priorities)

    @override
    def to_action_space(self) -> int:
        return list(permutations(self.possible_energy_feeds, len(self.possible_energy_feeds))).index(
            self.energy_feed_priority
        )

    def __repr__(self):
        return f"EnergyExcessAction({self.energy_feed_priority})"
