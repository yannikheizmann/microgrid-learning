from rl_microgrid.microgrid.components._battery import Battery
from ...config.configuration.microgrid import CarBatteryConfig


class CarBattery(Battery):
    """
    A class representing a battery of an electric car.

    Inherits from the generic Battery class and adds functionality to track a desired state of charge (SoC)
    at a specific future time, which can be used for planning energy usage or charging strategies.

    Attributes:
        desired_soc (float): The desired state of charge (between 0 and 1).
        target_time (int): The time (in seconds, minutes, or arbitrary units) by which the desired SoC should be reached.
    """

    def __init__(self, battery_config: CarBatteryConfig) -> None:
        """
        Initializes the car battery with the provided configuration arguments.
        Desired state of charge is initially set to None.

        Args:
            battery_config (BatteryConfig): An object containing the configuration arguments for the battery.
        """
        super().__init__(battery_config)
        self.desired_soc: float = battery_config.DESIRED_SOC
        self.target_time: int = battery_config.TARGET_TIME
        self.can_be_charged: bool = True
        self.time_away: int = battery_config.TIME_AWAY

    def needs_charging(self, time) -> float:
        time_factor = 0 if self.target_time == 0 else max(1 - (self.target_time - time), 0) / self.target_time
        soc_diff = 0 if self.desired_soc == 0 else max(self.desired_soc - self.SoC, 0) / self.desired_soc
        return time_factor * soc_diff

    def setCanBeCharged(self, value: bool):
        self.can_be_charged = value

    def setDesiredSoc(self, desired_soc):
        self.desired_soc = desired_soc

    def setTargetTime(self, target_time):
        self.target_time = target_time

    def charge(self, energy_input):
        if self.can_be_charged:
            return super().charge(energy_input)
        else:
            return energy_input

    def discharge(self, energy_output):
        if self.can_be_charged:
            return super().discharge(energy_output)
        else:
            return 0
