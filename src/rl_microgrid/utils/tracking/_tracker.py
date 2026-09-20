from enum import Enum

import wandb
from stable_baselines3.common.callbacks import BaseCallback, CallbackList
from wandb.integration.sb3 import WandbCallback
from pydantic import BaseModel

from ._callbacks import TensorboardCallback, EvaluationCallback
from ...config.configuration.args import Args
from ...config.configuration.static import TRACKING_PATH
from ...config.factory import EnvironmentFactory


def flatten(args: dict) -> dict:
    """Flatten a dict recursive to log with Tensorboard and W&B."""
    flattened_dict = {}
    for key, value in args.items():
        if isinstance(value, BaseModel):
            flattened_dict = flattened_dict | flatten(value.model_dump())
        elif isinstance(value, dict):
            flattened_dict = flattened_dict | flatten(value)
        elif isinstance(value, Enum):
            flattened_dict[key] = value.value
        elif isinstance(value, list):
            flattened_dict[key] = str(value)
        else:
            flattened_dict[key] = value
    return flattened_dict


class Tracker:
    def __init__(self, project_name: str, config: Args) -> None:
        """
        Initialize the W&B run.
        """
        self.project_name = project_name
        self.config = flatten(config.model_dump())

        self._eval_env = EnvironmentFactory.create(args=config)
        self._eval_freq = config.episodes // 5

        wandb.init(
            project=project_name,
            dir=TRACKING_PATH,
            config=config,
            sync_tensorboard=True,  # Sync SB3's TensorBoard logs to W&B (trakcs rewards, loss etc)
            monitor_gym=False,  # Automatically log environment videos
            save_code=True,  # Save the code state
        )

    def callbacks(self) -> BaseCallback:
        """
        Get the list of callbacks for W&B and custom metrics.
        """
        return CallbackList(
            [
                TensorboardCallback(self.project_name, self.config),
                EvaluationCallback(self._eval_env, eval_freq=self._eval_freq),
                WandbCallback(),
            ]
        )

    def finish(self) -> None:
        """
        Finish the W&B run.
        """
        wandb.finish()
