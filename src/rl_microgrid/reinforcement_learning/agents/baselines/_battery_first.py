from typing import TYPE_CHECKING

import numpy as np

from rl_microgrid.environment import MicrogridEnvironment
from rl_microgrid.microgrid.actions import (
    CompositeBasicAction,
    PriceAction,
    PriceLevel,
    EnergyExcessAction,
    EnergyFeed,
    EnergyDeficiencyAction,
    EnergySource,
)
from .._base import IAgent

if TYPE_CHECKING:
    from ....utils.tracking import Tracker


class BaselineBatteryFirstAgent(IAgent):
    def __init__(self, environment: MicrogridEnvironment) -> None:
        super().__init__(environment, None, 0)

        self.action = CompositeBasicAction(
            price_action=PriceAction(PriceLevel.MARKET_PRICE),
            energy_excess_action=EnergyExcessAction(
                [EnergyFeed.EXTERNAL_GRID, EnergyFeed.BATTERY],
                EnergyFeed.priority_order(EnergyFeed.BATTERY, EnergyFeed.EXTERNAL_GRID),
            ),
            energy_deficiency_action=EnergyDeficiencyAction(
                [EnergySource.EXTERNAL_GRID, EnergySource.BATTERY],
                EnergySource.priority_order(EnergySource.BATTERY, EnergySource.EXTERNAL_GRID),
            ),
        )

    def _load_model(self, model_path: str) -> None:
        pass

    def _act(self, observation: np.ndarray, deterministic: bool = False) -> int:
        # Always repeat the same action
        return self.action.to_action_space()

    def train(self, n_episodes: int, output_path: str, tracker: "Tracker", *args, **kwargs) -> None:
        pass
