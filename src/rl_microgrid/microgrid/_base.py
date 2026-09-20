from abc import abstractmethod, ABC
from typing import Type

import numpy as np

from rl_microgrid.config.registry import RegistryMeta
from .actions import IAction


class IMicrogrid(ABC, metaclass=RegistryMeta["IMicrogrid"]):
    action_type: Type[IAction]

    def __init__(self, action_type: Type[IAction]):
        self.action_type = action_type

    def action(self, action: int, time_step: int):
        action = self.action_type.from_action_space(action)
        # TODO use this to see how the model decides
        # print(f"Action: {action:02d} [{repr(action)}]")
        return action.execute(microgrid=self, time_step=time_step)

    def calc_action_space(self) -> int:
        return self.action_type.calc_action_space()

    @classmethod
    @abstractmethod
    def calc_observation_space(cls) -> tuple[int]:
        pass

    @abstractmethod
    def vectorize(self, day, iteration, time_step: int) -> np.ndarray:
        """Returns a Numpy-array filled with the attributes of the class"""
        pass

    @abstractmethod
    def before_step(self, day: int, iterations: int, time_step: int) -> None:
        pass

    @abstractmethod
    def reset(self) -> None:
        pass

    @abstractmethod
    def info(self, day: int, iterations: int, time_step: int) -> dict:
        pass
