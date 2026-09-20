from typing import override

from .. import IResidentialLoadsFactory
from rl_microgrid.microgrid.components import ResidentialLoad


class BasicResidentialLoadsFactory(IResidentialLoadsFactory):
    @classmethod
    @override
    def create(cls, num_loads: int) -> list[ResidentialLoad]:
        # different config / random values for each load
        return [ResidentialLoad(cls._get_config()) for _ in range(num_loads)]
