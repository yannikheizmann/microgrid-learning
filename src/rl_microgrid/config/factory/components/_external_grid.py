from typing import override

from .. import IExternalGridFactory
from rl_microgrid.microgrid.components import ExternalGrid


class BasicExternalGridFactory(IExternalGridFactory):
    @classmethod
    @override
    def create(cls) -> ExternalGrid:
        external_grid_config = cls._get_config()
        return ExternalGrid(external_grid_config)
