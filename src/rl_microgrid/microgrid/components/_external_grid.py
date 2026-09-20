import numpy as np
from numpy.typing import NDArray

from ...config.configuration.microgrid import ExternalGridConfig


class ExternalGrid:
    """
    A class representing an external grid for energy import and export.

    This class models an external grid where energy can be bought or sold, with associated pricing
    and fee structures. The class calculates the current price for selling or buying energy based on
    time-dependent prices and applies associated export and import fees.

    Attributes:
        _sell_prices (NDArray[np.float64]): Array of sell prices (in € per kWh) for exporting energy to the grid.
        _buy_prices (NDArray[np.float64]): Array of buy prices (in € per kWh) for importing energy from the grid.
        _export_fees (float): Fees (in € per kWh) charged for exporting energy to the grid.
        _import_fees (float): Fees (in € per kWh) charged for importing energy from the grid.
        _time (int): The current time index, representing the timestep in the simulation.

    """

    def __init__(self, external_grid_config: ExternalGridConfig) -> None:
        """
        Initializes the external grid with the provided configuration arguments. The time index is initialized to zero.

        Args:
            external_grid_config (ExternalGridConfig): An object containing the configuration arguments for the external grid,
                                                    including sell prices, buy prices, and export/import fees.
        """
        self._sell_prices: NDArray[np.float64] = external_grid_config.SELL_PRICES
        self._buy_prices: NDArray[np.float64] = external_grid_config.BUY_PRICES
        self._export_fees: float = external_grid_config.EXPORT_FEES
        self._import_fees: float = external_grid_config.IMPORT_FEES
        self._time: int = 0

    @property
    def current_sell_price(self) -> float:
        """
        Returns the current sell price for exporting energy, including the export fee.
        The current sell price is determined by the sell price at the current time index (`_time`) plus the export fee.

        Returns:
            float: The current price per kWh for exporting energy, including the export fee.
        """
        return self._sell_prices[self._time] + self._export_fees

    @property
    def current_time(self) -> int:
        """
        Get current time

        Returns:
            int: current time of the grid
        """
        return self._time

    @property
    def current_buy_price(self) -> float:
        """
        Returns the current buy price for importing energy, including the import fee.
        The current buy price is determined by the buy price at the current time index (`_time`) plus the import fee.

        Returns:
            float: The current price per kWh for importing energy, including the import fee.
        """
        return self._buy_prices[self._time] + self._import_fees

    def sell(self, energy_amount: int) -> float:
        """
        Calculates the total income from selling a given amount of energy to the grid.

        Args:
            energy_amount (int): The amount of energy (in kWh) to sell to the grid.

        Returns:
            float: The total income from selling the energy (in €).
        """
        return self.current_sell_price * energy_amount

    def buy(self, energy_amount: int) -> float:
        """
        Calculates the total cost of buying a given amount of energy from the grid.

        Args:
            energy_amount (int): The amount of energy (in kWh) to buy from the grid.

        Returns:
            float: The total cost of buying the energy (in €).
        """
        return -self.current_buy_price * energy_amount

    def set_time(self, time: int) -> None:
        """
        Sets the current time index for accessing time-dependent prices.

        Args:
            time (int): The time index to set, representing the timestep in the simulation.
        """
        self._time = time

    def total_cost(self, prices: list[float], energy: list[float]) -> float:
        """
        Calculates the total cost for a list of energy prices and amounts, including import fees.

        Args:
            prices (list[float]): A list of buy prices (in € per kWh) for each timestep.
            energy (list[float]): A list of energy amounts (in kWh) to import for each timestep.

        Returns:
            float: The total cost for importing the specified energy amounts, including import fees.
        """
        return sum(
            (price_i * energy_i / 100 + self._import_fees * energy_i) for price_i, energy_i in zip(prices, energy)
        )

    def get_buy_price(self, time):
        """Returns the current buy and sell prices as a numpy array"""
        return self._buy_prices[time]

    def get_sell_price(self, time):
        """Returns the current buy and sell prices as a numpy array"""
        return self._sell_prices[time]
