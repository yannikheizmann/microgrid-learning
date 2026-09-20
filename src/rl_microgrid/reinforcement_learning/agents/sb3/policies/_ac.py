import torch

from stable_baselines3.ppo.policies import ActorCriticPolicy

from ._base import IBrainPolicy
from ....brains import IBrain


class ActorCriticBrainPolicy(IBrainPolicy, ActorCriticPolicy):
    def __init__(self, observation_space, action_space, lr_schedule, brain: IBrain):
        IBrainPolicy.__init__(self, observation_space, action_space, lr_schedule, brain)

    @classmethod
    def _get_sb3_policy(cls) -> ActorCriticPolicy:
        return ActorCriticPolicy

    def forward(self, obs, deterministic: bool = True):
        outputs = self._brain(obs)
        logits, value = outputs
        return logits, value

    def _predict(self, obs, deterministic: bool = True):
        logits, _ = self.forward(obs, deterministic)
        action_probs = torch.softmax(logits, dim=-1)
        if deterministic:
            actions = action_probs.argmax(dim=1)
        else:
            actions = torch.multinomial(action_probs, num_samples=1)
        return actions
