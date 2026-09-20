from typing import override

from .. import IDERFactory
from rl_microgrid.microgrid.components import DistributedEnergyResources


class BasicDERFactory(IDERFactory):
    @classmethod
    @override
    def create(cls) -> DistributedEnergyResources:
        der_config = cls._get_config()
        return DistributedEnergyResources(der_config)
