import numpy as np
from numpy.typing import NDArray
import random

from ...config.configuration.microgrid import ResidentialLoadConfig


class ResidentialLoad:
    def __init__(self, residential_load_config: ResidentialLoadConfig) -> None:
        self._base_load: NDArray[np.float64] = residential_load_config.BASE_LOAD
        self._sensitivity: float = residential_load_config.SENSITIVITY
        self._patience = max(residential_load_config.PATIENCE, 1)
        self._shifted_load: NDArray[np.float64] = np.zeros(24, dtype=float)
        self._adjusted_current_load: float = self._base_load[0]
        self._shifted_loads_dict: dict[int, int] = {}

    def react(self, price_tier, current_time: int) -> float:
        # If price_tier is an enum, get its value
        if hasattr(price_tier, "value"):
            price_tier = price_tier.value

        self._adjusted_current_load = self._base_load[current_time]
        load_response = self._sensitivity * (price_tier - 2)
        if load_response != 0:
            self._adjusted_current_load -= self._base_load[current_time] * load_response
            self._shifted_loads_dict[current_time] = self._base_load[current_time] * load_response
        for time in list(self._shifted_loads_dict.keys()):  # Convert to list to avoid dict changed during iteration
            price_effect = -self._shifted_loads_dict[time] * (price_tier - 2)
            time_effect = (current_time - time) / self._patience
            probability_of_execution = price_effect + time_effect
            if random.random() <= probability_of_execution:
                self._adjusted_current_load += self._shifted_loads_dict[time]
                del self._shifted_loads_dict[time]

        return max(0, self._adjusted_current_load)

    def _get_shift_factor(self, price_level: int) -> float:
        normalized_price_level = (price_level + 3) / 4
        shift_factor = self._sensitivity * normalized_price_level
        return shift_factor

    def shift(self, shift_time: int, price_level: int, current_time: int) -> float:
        # get shift factor determining how much of the current load is shifted
        shift_factor = self._get_shift_factor(price_level)
        # shift loads
        shift_target_time = (current_time + shift_time) % 24
        self._shifted_load[shift_target_time] = shift_factor * self._base_load[current_time]
        # return adjusted current load
        self._adjusted_current_load = (1 - shift_factor) * self._base_load[current_time] + self._shifted_load[
            current_time
        ]
        return self._adjusted_current_load

    def get_normalized_load(self) -> float:
        min_load = np.min(self._base_load)
        max_load = np.max(self._base_load)

        if min_load == max_load:
            return 0.5

        normalized_load = float(self._adjusted_current_load - min_load) / float(max_load - min_load)
        return normalized_load

    # TODO Still needed?
    def load(self) -> float:
        """For rendering purposes"""
        return max(0.0, self._adjusted_current_load)

    # TODO Still needed?
    def get_base_load(self):
        """For rendering purposes"""
        return self._base_load
