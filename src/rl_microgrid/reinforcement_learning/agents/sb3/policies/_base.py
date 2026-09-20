from abc import ABC

from stable_baselines3.common.policies import BasePolicy


class IBrainPolicy(BasePolicy, ABC):
    pass
