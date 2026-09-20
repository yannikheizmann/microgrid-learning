from __future__ import annotations
from stable_baselines3 import DQN
import numpy as np
from typing import override

from ._base import ISB3Agent
from .policies import DQNBrainPolicy
from rl_microgrid.environment import MicrogridEnvironment
from ...brains import IBrain
from ....config.configuration.static import TENSORBOARD_PATH


class SB3_DQNAgent(ISB3Agent):
    def __init__(
        self,
        environment: MicrogridEnvironment,
        brain: IBrain,
        batch_size: int,
        learning_rate: float,
        gamma: float,
        exploration_initial_eps: float,
        exploration_final_eps: float,
        exploration_fraction: float,
        target_update_interval: int,
        memory_size: int = 10000,
    ):
        self._memory_size = memory_size
        self._gamma = gamma
        self._exploration_initial_eps = exploration_initial_eps
        self._exploration_final_eps = exploration_final_eps
        self._exploration_fraction = exploration_fraction
        self._target_update_interval = target_update_interval
        super().__init__(environment, brain, batch_size, learning_rate)

    @override
    def _instantiate_model(self) -> DQN:
        model = DQN(
            DQNBrainPolicy,
            env=self._environment,
            learning_rate=self._learning_rate,
            batch_size=self._batch_size,
            buffer_size=self._memory_size,
            gamma=self._gamma,
            target_update_interval=self._target_update_interval,
            verbose=1,
            policy_kwargs=self._get_policy_kwargs(),
            tensorboard_log=TENSORBOARD_PATH,
            exploration_initial_eps=self._exploration_initial_eps,
            exploration_final_eps=self._exploration_final_eps,
            exploration_fraction=self._exploration_fraction,
        )
        return model

    @override
    def _load_model(self, model_path: str) -> None:
        self._model = DQN.load(model_path, policy=DQNBrainPolicy)

    @override
    def _act(self, observation: np.ndarray, deterministic: bool = False) -> int:
        action, _ = self._model.predict(observation, deterministic=deterministic)
        return int(action)
