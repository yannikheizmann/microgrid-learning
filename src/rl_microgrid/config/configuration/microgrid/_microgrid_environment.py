from pydantic import Field

from . import IConfig


# -- MICROGRID ENVIRONMENT -----------------------------------------------------------
class MicrogridEnvironmentConfig(IConfig):
    """
    **A class representing the configuration arguments for a microgrid environment.**
    This class holds the configuration parameters required to define the behavior of a microgrid environment,
    including iterations, day range, market price, and power cost.

    Attributes:
        iterations (int): Length of one episode.
        min_day (int): Starting day.
        max_day (int): Ending day.
        market_price (float): Market price per kWh.
        power_cost (float): Power cost per kWh.
    """

    ITERATIONS: int = Field(
        default=24,
        description="Length of one episode.",
    )
    MIN_DAY: int = Field(
        default=0,
        description="Starting day.",
    )
    MAX_DAY: int = Field(
        default=100,
        description="Ending day.",
    )
    MARKET_PRICE: float = Field(
        default=5.48,
        description="Market price per kWh.",
    )
    POWER_COST: float = Field(
        default=3.2,
        description="Power cost per kWh.",
    )
