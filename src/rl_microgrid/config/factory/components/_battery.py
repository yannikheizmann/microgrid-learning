from typing import override

from .. import IBatteryFactory
from rl_microgrid.microgrid.components import Battery


class BasicBatteryFactory(IBatteryFactory):
    @classmethod
    @override
    def create(cls) -> Battery:
        battery_config = cls._get_config()
        return Battery(battery_config)
