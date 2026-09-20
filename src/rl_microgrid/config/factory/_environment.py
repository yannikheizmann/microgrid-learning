import gymnasium as gym

from ...environment import MicrogridEnvironment
from ..registry import Registry
from ...config.configuration.args import Args
from ...config.configuration.microgrid import MicrogridEnvironmentConfig


class EnvironmentFactory:
    @classmethod
    def create(
        cls,
        args: Args,
    ) -> gym.Env:
        RewardClass = Registry.get("IReward", args.reward.value)
        MicrogridFactoryClass = Registry.get("IMicrogridFactory", args.microgrid.value)
        environment = MicrogridEnvironment(
            env_config=MicrogridEnvironmentConfig(),
            microgrid_factory=MicrogridFactoryClass,
            reward=RewardClass,
        )
        return environment
