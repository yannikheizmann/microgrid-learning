from typing import override
import gymnasium as gym
from stable_baselines3.dqn.policies import DQNPolicy, QNetwork
from stable_baselines3.common.torch_layers import FlattenExtractor
from stable_baselines3.common.preprocessing import get_flattened_obs_dim
from stable_baselines3.common.type_aliases import Schedule

from ._base import IBrainPolicy
from ....brains import IBrain


class CustomQNetwork(QNetwork):
    def __init__(
        self,
        observation_space: gym.spaces.Space,
        action_space: gym.spaces.Discrete,
        brain: IBrain,
    ) -> None:
        super().__init__(
            observation_space=observation_space,
            action_space=action_space,
            features_extractor=FlattenExtractor(observation_space),
            features_dim=get_flattened_obs_dim(observation_space),
        )
        self.q_net = brain.get_net()


class DQNBrainPolicy(IBrainPolicy, DQNPolicy):
    def __init__(
        self,
        observation_space: gym.spaces.Box,
        action_space: gym.spaces.Discrete,
        lr_schedule: Schedule,
        brain: IBrain,
    ) -> None:
        self._brain = brain
        DQNPolicy.__init__(self, observation_space, action_space, lr_schedule)

    @override
    def make_q_net(self):
        q_net = CustomQNetwork(
            observation_space=self.observation_space,
            action_space=self.action_space,
            brain=self._brain,
        )
        return q_net
