import math

from ...config.configuration.microgrid import BatteryConfig


class Battery:
    """
    A class representing a rechargeable battery storage system.

    This system models energy storage with various parameters affecting its charging, discharging,
    and dissipation behavior.

    Attributes:
        _capacity (int): Total battery capacity in kWh.
        _discharge_coefficient (float): Battery discharge efficiency coefficient.
        _dissipation_coefficient (float): Battery energy dissipation, i.e., energy lost over time, expressed as a fraction.
        _charging_rate (float): Maximum battery charging rate as a proportion of its total capacity per charging cycle (unitless).
        _max_discharge (int): Maximum allowable discharge rate in kW.
        _max_energy_input (int): Maximum energy input per charging cycle in kWh.
        _remaining_charge (int): The current stored energy in the battery in kWh.
    """

    def __init__(self, battery_config: BatteryConfig) -> None:
        """
        Initializes the battery with the provided configuration arguments. The initial charge is set to zero.

        Args:
            battery_config (BatteryConfig): An object containing the configuration arguments for the battery.
                                        This includes capacity, discharge coefficient, dissipation coefficient,
                                        charging rate, max discharge rate, and max energy input.
        """
        self._capacity: int = battery_config.CAPACITY
        self._discharge_coefficient: float = battery_config.DISCHARGE_COEFFICIENT
        self._dissipation_coefficient: float = battery_config.DISSIPATION_COEFFICIENT
        self._charging_rate: float = battery_config.CHARGING_RATE
        self._max_discharge: int = battery_config.MAX_DISCHARGE
        self._max_energy_input: int = battery_config.MAX_ENERGY_INPUT
        self._remaining_charge: int = 0

    @property
    def is_full(self) -> bool:
        """
        Checks whether the battery is full based on its remaining charge.

        Returns:
            bool: True if the battery is full (i.e., the remaining charge is greater than or equal to capacity),
              otherwise False.
        """
        return self._remaining_charge >= self._capacity

    @property
    def SoC(self) -> float:
        """
        Calculates the state of charge (SoC) of the battery.
        The state of charge is calculated as the ratio of the remaining charge to the total capacity.

        Returns:
            float: The state of charge (SoC) as a fraction of the total capacity (between 0 and 1).
        """
        return self._remaining_charge / self._capacity

    @property
    def SoC_kWh(self):
        """
        Get the current remaining charge of the battery in kWh.

        Returns:
            float: Remaining charge of the battery in kWh.
        """
        return self._remaining_charge

    def charge(self, energy_input: int) -> int:
        """
        Charges the battery with the provided energy input.

        The battery is charged at a rate determined by the `charging_rate` until it reaches its full capacity or
        until the maximum energy input is reached. If the battery is already full, the method will return the
        unspent energy.

        Args:
            energy_input (int): The amount of energy (in kWh) to input into the battery.

        Returns:
            int: The amount of energy (in kWh) that could not be charged to the battery due to it being full or
                exceeding the maximum allowed energy input for the charging cycle.
        """
        if self.is_full:
            return energy_input
        else:
            self._remaining_charge += self._charging_rate * min(energy_input, self._max_energy_input)
            leftover = self._remaining_charge - self._capacity + max(energy_input - self._max_energy_input, 0)
            self._remaining_charge = min(self._capacity, self._remaining_charge)
            return max(leftover, 0)

    def discharge(self, energy_output: int) -> int:
        """
        Discharges the battery by the specified amount of energy.

        The battery will discharge up to the maximum discharge rate or the current remaining charge, whichever is
        lower. The discharged energy is then adjusted based on the battery's discharge efficiency.

        Args:
            energy_output (int): The desired amount of energy (in kWh) to discharge from the battery.

        Returns:
            int: The amount of energy (in kWh) actually discharged, adjusted for the discharge efficiency.
        """
        discharge_amount = min(energy_output, self._remaining_charge, self._max_discharge)
        self._remaining_charge -= discharge_amount
        return discharge_amount * self._discharge_coefficient

    def dissipate(self) -> None:
        """
        Simulates the self-discharge of the battery over time.

        The remaining charge of the battery is reduced based on the dissipation coefficient, which represents
        the rate at which energy is lost due to self-discharge.

        The charge is updated by applying the exponential decay formula to simulate the gradual loss of energy.
        """
        self._remaining_charge = self._remaining_charge * math.exp(-self._dissipation_coefficient)

    def reset(self) -> None:
        """
        Resets the battery's remaining charge to zero.
        """
        self._remaining_charge = 0
