from typing import override

from . import IMicrogridFactory
from .components import (
    BasicBatteryFactory,
    BasicExternalGridFactory,
    BasicResidentialLoadsFactory,
    BasicDERFactory,
    BasicCarBatteryFactory,
)
from rl_microgrid.microgrid import IMicrogrid, BasicMicrogrid, CarBatteryMicrogrid


class BasicMicrogridFactory(IMicrogridFactory):
    @classmethod
    @override
    def create(cls) -> IMicrogrid:
        micro_grid_config = cls._get_config()
        battery = BasicBatteryFactory.create()
        external_grid = BasicExternalGridFactory.create()
        residential_loads = BasicResidentialLoadsFactory.create(micro_grid_config.NUM_LOADS)
        distributed_energy_resources = BasicDERFactory.create()
        return BasicMicrogrid(
            battery=battery,
            external_grid=external_grid,
            residential_loads=residential_loads,
            distributed_energy_resources=distributed_energy_resources,
        )


class CarBatteryMicrogridFactory(IMicrogridFactory):
    @classmethod
    @override
    def create(cls) -> IMicrogrid:
        micro_grid_config = cls._get_config()
        battery = BasicBatteryFactory.create()
        car_battery = BasicCarBatteryFactory.create()
        external_grid = BasicExternalGridFactory.create()
        residential_loads = BasicResidentialLoadsFactory.create(micro_grid_config.NUM_LOADS)
        distributed_energy_resources = BasicDERFactory.create()
        return CarBatteryMicrogrid(
            battery=battery,
            external_grid=external_grid,
            residential_loads=residential_loads,
            distributed_energy_resources=distributed_energy_resources,
            car_battery=car_battery,
        )
