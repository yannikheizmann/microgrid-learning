from enum import Enum
from typing import override, TYPE_CHECKING

from ._base import IAction

if TYPE_CHECKING:
    from .. import IMicrogrid


class PriceLevel(Enum):
    """Level of price difference to apply on the market-price, enabling the action for price elasticity.

    DECREASE will decrease the default market price
    MARKET_PRICE will take the market price as it is
    INCREASE will increase the default market price
    """

    SIGNIFICANT_DECREASE = -3
    SLIGHT_DECREASE = -1.5
    MARKET_PRICE = 0
    SLIGHT_INCREASE = 1.5
    SIGNIFICANT_INCREASE = 3


class PriceAction(IAction):
    """Given the price_level, the action calculates the total load demand to exploit the household's price elasticity.

    Attributes:
        price_level (PriceLevel): the price level
    """

    def __init__(self, price_level: PriceLevel):
        super().__init__()
        self.price_level: PriceLevel = price_level

    @override
    def execute(self, microgrid: "IMicrogrid", time_step: int) -> float:
        """React to all residential loads of the microgrid and sum up the total load demand.

        Args:
            microgrid: environment to manipulate
            time_step: current time step in hours

        Returns:
            The total load demand
        """
        total_loads = sum(
            map(
                lambda load: load.react(self.price_level, time_step % 24),
                microgrid.residential_loads,
            )
        )

        return total_loads

    @classmethod
    @override
    def calc_action_space(cls) -> int:
        """Calculates the size of the action space.
        Determined by the available PriceLevels.

        Returns:
            size of the action space
        """
        return len(PriceLevel)

    @classmethod
    @override
    def from_action_space(cls, action: int, **kwargs) -> "PriceAction":
        """Factory method for creating a PriceAction object for a given action inside the action space.

        Args:
            action (int): the action index. Required to be in range [0, action_space)

        Returns:
            PriceAction instance

        Raises:
            ValueError: if the action index is out of range
        """
        if action < 0 or action >= cls.calc_action_space():
            raise ValueError(f"Action ({action}) has to be in range [0, {cls.calc_action_space()})")
        price_level = list(PriceLevel)[action]
        return cls(price_level)

    @override
    def to_action_space(self) -> int:
        return list(PriceLevel).index(self.price_level)

    def __repr__(self):
        return f"PriceAction({self.price_level})"
