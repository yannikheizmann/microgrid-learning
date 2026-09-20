from abc import ABC, abstractmethod
from typing import TypeVar, TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    from .. import IMicrogrid


class ActionResult(BaseModel):
    energy_used: float | None = None
    energy_bought: float | None = None
    energy_sold: float | None = None
    price: float | None = None


T = TypeVar("T")


class IAction(ABC):
    """
    Base interface for all possible actions.
    An Action needs to implement ``execute(microgrid, step)`` to define how it interacts with the environment.
    """

    @abstractmethod
    def execute(self, microgrid: "IMicrogrid", time_step: int):
        """Execute the action on the given environment.

        Args:
            microgrid: environment to manipulate
            time_step: current time step in hours

        Returns:
            Information about how the environment was manipulated. May be used for calculating the reward.
        """
        pass

    @classmethod
    @abstractmethod
    def calc_action_space(cls, **kwargs) -> int:
        """Calculates the size for the action space, needed for this action.

        Returns:
             size of the action space
        """
        pass

    @classmethod
    @abstractmethod
    def from_action_space(cls, action: int, **kwargs) -> "IAction":
        """Factory method for creating an action object for a given action inside the action space.

        Example:
            >>> import numpy as np
            >>> prediction = np.array([0.2, 0.1, 0.7]) # Prediction of a net. Must match size of #calc_action_space()
            >>> action = np.argmax(prediction)
            >>> specific_action = SpecificAction.from_action_space(action)

        Args:
            action: index of the action to create

        Returns:
            instance of the called Action class
        """
        pass

    @abstractmethod
    def to_action_space(self) -> int:
        pass
