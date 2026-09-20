from abc import ABC, abstractmethod
import gymnasium as gym
from typing import override, TYPE_CHECKING
from stable_baselines3.common.base_class import BaseAlgorithm
import numpy as np

from .._base import IAgent
from ...brains import IBrain

if TYPE_CHECKING:
    from ....utils.tracking import Tracker


class ISB3Agent(IAgent, ABC):
    """Base class for SB3 agents."""

    def __init__(
        self,
        environment: gym.Env,
        brain: IBrain,
        batch_size: int,
        learning_rate: float,
    ) -> None:
        IAgent.__init__(self, environment, brain, batch_size)
        self._learning_rate = learning_rate
        self._model = self._instantiate_model()

    def _get_policy_kwargs(self) -> dict:
        kwargs = {"brain": self._brain}
        return kwargs

    @abstractmethod
    def _load_model(self, model_path: str) -> None:
        pass

    @abstractmethod
    def _act(self, observation: np.ndarray, deterministic: bool = False):
        pass

    @abstractmethod
    def _instantiate_model(self) -> BaseAlgorithm:
        pass

    @override
    def train(
        self,
        n_episodes: int,
        output_path: str,
        tracker: "Tracker",
        *args,
        **kwargs,
    ) -> None:
        self._model.learn(total_timesteps=n_episodes, callback=tracker.callbacks())
        output_model_path = f"{output_path}/microgrid_model.pth"
        self._model.save(output_model_path)
