from abc import abstractmethod
from typing import Union, Any

import gymnasium as gym
from stable_baselines3.common.callbacks import BaseCallback, EvalCallback
from stable_baselines3.common.logger import HParam, Figure
import wandb
from stable_baselines3.common.vec_env import VecEnv
from wandb.integration.sb3 import WandbCallback

from rl_microgrid.utils import MicrogridEnvironmentPlot


class BaseInfoCallback(BaseCallback):
    @classmethod
    def _info_keywords(cls) -> tuple[str, ...]:
        """
        Get the keywords to monitor for episode-level metrics.
        """
        return (
            "reward",
            "energy_generated",
            "battery_kWh",
            "energy_sold",
            "energy_bought",
            "carbattery_kWh",
        )

    def _on_step(self) -> bool:
        # Access the 'infos' from the current step
        infos = self.locals.get("infos", [])
        if infos:
            # Assuming a single environment; adjust indexing for multiple environments
            info = infos[0]
            log_dict = {key: info[key] for key in self._info_keywords() if key in info}
            self._on_step_info(log_dict)
        return True

    @abstractmethod
    def _on_step_info(self, info: dict) -> None:
        pass


class TensorboardCallback(BaseInfoCallback):
    """
    Custom callback for plotting additional values in tensorboard.
    """

    def __init__(self, project_name: str, config: dict, verbose=0):
        super().__init__(verbose)
        self.project_name = project_name
        self.config = config

    def _on_training_start(self) -> None:
        # define the metrics that will appear in the `HPARAMS` Tensorboard tab by referencing their tag
        # Tensorbaord will find & display metrics from the `SCALARS` tab
        # TODO metric values are not shown
        metric_dict = {
            "rollout/ep_len_mean": 0.0,
            "rollout/ep_rew_mean": 0.0,
            "train/loss": 0.0,
            "train/reward": 0.0,
        }
        self.logger.record(
            "hparams",
            HParam(self.config, metric_dict),
            exclude=("stdout", "log", "json", "csv"),
        )

    def _on_step_info(self, info: dict) -> None:
        for key, value in info.items():
            self.logger.record(f"train/{key}", value)


class EvaluationCallback(EvalCallback):
    def __init__(
        self,
        eval_env: Union[gym.Env, VecEnv],
        n_eval_episodes: int = 24 * 10,
        eval_freq: int = 1000,
    ):
        self._plot_callback = PlotCallback(n_eval_episodes // 24)
        super().__init__(
            eval_env=eval_env,
            callback_on_new_best=None,
            callback_after_eval=self._plot_callback,
            n_eval_episodes=n_eval_episodes,
            eval_freq=eval_freq,
            log_path=None,  # TODO
            best_model_save_path=None,  # TODO
            deterministic=True,
            render=False,
            verbose=1,
            warn=True,
        )

    def _log_success_callback(self, locals_: dict[str, Any], globals_: dict[str, Any]) -> None:
        super()._log_success_callback(locals_, globals_)

        info = locals_["info"]
        self._plot_callback.collect(info)


class PlotCallback(BaseCallback):
    def __init__(self, days: int, verbose: int = 0):
        super().__init__(verbose)
        self._env_plot = MicrogridEnvironmentPlot(days)

    def collect(self, info: dict[str, Any]):
        self._env_plot.collect_info(info)

    def reset(self):
        self._env_plot.reset()

    def _on_step(self) -> bool:
        figure = self._env_plot.plot_figure()
        self.logger.record(
            "eval/plot",
            Figure(figure, close=True),
            exclude=("stdout", "log", "json", "csv"),
        )
        self._env_plot.reset()
        return True


# Currently not used.
# Infos are logged via Tensorboard and these are collected from wandb automatically.
class CustomWandbCallback(WandbCallback, BaseInfoCallback):
    def __init__(self, verbose=0):
        super().__init__(verbose)

    def _on_step(self) -> bool:
        return super()._on_step()  # Call both, the original WandbCallback's and BaseInfoCallback's method

    def _on_step_info(self, info: dict) -> None:
        wandb.log(info)
