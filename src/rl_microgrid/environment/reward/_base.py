from abc import ABC, abstractmethod

from ...microgrid.actions import CompositeResult
from .. import MicrogridEnvironment
from ...config.registry import (
    RegistryMeta,
)


class IReward(ABC, metaclass=RegistryMeta["IReward"]):
    """Base class to define concrete reward functions."""

    @classmethod
    @abstractmethod
    def calculate_reward(
        cls,
        env: MicrogridEnvironment,
        action_result: CompositeResult,
    ) -> float:
        """
        Calculates the reward for a given transition.
        To be called from env.step().

        Args:
            env: The current environment.
            action_result: The result of the action executed just before.

        Returns:
            A float representing the reward.
        """
        pass
