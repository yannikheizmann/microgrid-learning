from __future__ import annotations

import random
from typing import override, Any, Type, TYPE_CHECKING

import gymnasium as gym
import numpy as np

from ..config.configuration.microgrid import MicrogridEnvironmentConfig
from ..config.factory import IMicrogridFactory

if TYPE_CHECKING:
    from ..environment import IReward


class MicrogridEnvironment(gym.Env):
    def __init__(
        self,
        env_config: MicrogridEnvironmentConfig,
        microgrid_factory: Type[IMicrogridFactory],
        reward: Type[IReward],
    ):
        self.iterations = env_config.ITERATIONS
        self.min_day = env_config.MIN_DAY
        self.max_day = env_config.MAX_DAY
        self.market_price = env_config.MARKET_PRICE
        self.power_cost = env_config.POWER_COST
        self.microgrid_factory = microgrid_factory
        self.reward = reward
        self.day = self.min_day
        self.time_step = 0

        # TODO missing: power_generation, high_price

        self.microgrid = self.microgrid_factory.create()

        # Determine the actual shape of the observation space by getting a sample observation
        sample_obs = self.microgrid.vectorize(self.day, self.iterations, 1)
        observation_shape = sample_obs.shape
        print(f"DEBUG: Sample observation shape: {observation_shape}")

        # Get the dimension for action space by creating a dummy CompositeAction
        self.action_space = gym.spaces.Discrete(self.microgrid.calc_action_space())

        # Define observation space to match the actual observation shape
        self.observation_space = gym.spaces.Box(
            low=-100,
            high=100,
            dtype=np.float32,
            shape=observation_shape,  # Use the actual shape
        )

    @override
    def step(self, action: int):
        self.microgrid.before_step(self.day, self.iterations, self.time_step)

        self.action_result = self.microgrid.action(action, self.time_step)

        # calculate reward
        reward = self.reward.calculate_reward(self, self.action_result)

        # move timestep
        self.time_step += 1

        # check if terminated
        terminal = self.time_step == self.iterations

        # return new observation, reward, if terminated, (info)
        observation = self.microgrid.vectorize(self.day, self.iterations, self.time_step)

        info = {
            "reward": reward,
            "price": self.action_result.price_level.value + self.market_price,
            "energy_sold": self.action_result.energy_sold,
            "energy_bought": self.action_result.energy_bought,
            "action": str(action),
        }
        info = info | self.microgrid.info(self.day, self.iterations, self.time_step)
        return observation, reward, terminal, False, info

    @override
    def reset(self, *, seed: int | None = None, options: dict[str, Any] | None = None) -> tuple[np.ndarray, dict]:
        super().reset(seed=seed, options=options)
        if seed is None:
            self.day = random.randint(self.min_day, self.max_day)
        else:
            self.day = seed
        self.time_step = 0
        # TODO self.high_price = 0, dont know if high_price is needed actually
        # removed because otherwise e.g. battery SoC is not transfered to next day
        # self.microgrid_factory.create()
        self.microgrid.reset()
        state = self.microgrid.vectorize(self.day, self.iterations, self.time_step)
        return state, {}

    @override
    def close(self):
        """
        Nothing to be done here, but has to be defined
        """
        return

    def get_observation_dim(self) -> int:
        """
        Returns the dimension of the observation space
        """
        return self.observation_space.shape[0]

    def get_action_dim(self) -> int:
        """
        Returns the dimension of the action space
        """
        return self.action_space.n
