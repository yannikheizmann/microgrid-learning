from abc import ABC, abstractmethod

from rl_microgrid.microgrid import (
    IMicrogrid,
    Battery,
    ExternalGrid,
    ResidentialLoad,
    DistributedEnergyResources,
    CarBattery,
)
from ..configuration.microgrid import (
    MicrogridConfig,
    BatteryConfig,
    ExternalGridConfig,
    DERConfig,
    ResidentialLoadConfig,
    CarBatteryConfig,
)
from ..registry import (
    RegistryMeta,
)


class IBatteryFactory(ABC):
    @classmethod
    def _get_config(cls) -> BatteryConfig:
        return BatteryConfig()

    @classmethod
    @abstractmethod
    def create(cls) -> Battery:
        pass


class ICarBatteryFactory(ABC):
    @classmethod
    def _get_config(cls) -> CarBatteryConfig:
        return CarBatteryConfig()

    @classmethod
    @abstractmethod
    def create(cls) -> CarBattery:
        pass


class IExternalGridFactory(ABC):
    @classmethod
    def _get_config(cls) -> ExternalGridConfig:
        return ExternalGridConfig()

    @classmethod
    @abstractmethod
    def create(cls) -> ExternalGrid:
        pass


class IResidentialLoadsFactory(ABC):
    @classmethod
    def _get_config(cls) -> ResidentialLoadConfig:
        return ResidentialLoadConfig()

    @classmethod
    @abstractmethod
    def create(cls) -> list[ResidentialLoad]:
        pass


class IDERFactory(ABC):
    @classmethod
    def _get_config(cls) -> DERConfig:
        return DERConfig()

    @classmethod
    @abstractmethod
    def create(cls) -> DistributedEnergyResources:
        pass


class IMicrogridFactory(ABC, metaclass=RegistryMeta["IMicrogridFactory"]):
    @classmethod
    def _get_config(cls) -> MicrogridConfig:
        return MicrogridConfig()

    @classmethod
    @abstractmethod
    def create(cls) -> IMicrogrid:
        pass
