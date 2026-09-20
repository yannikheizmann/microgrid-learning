from typing import override

from .. import ICarBatteryFactory
from rl_microgrid.microgrid.components import CarBattery


class BasicCarBatteryFactory(ICarBatteryFactory):
    @classmethod
    @override
    def create(cls) -> CarBattery:
        car_battery_config = cls._get_config()
        return CarBattery(car_battery_config)
