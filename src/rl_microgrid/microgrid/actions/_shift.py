from __future__ import annotations
from enum import Enum
from typing import override, TYPE_CHECKING

from ._base import IAction

if TYPE_CHECKING:
    from .. import IMicrogrid


class PriceLevel(Enum):
    SIGNIFICANT_DECREASE = -2
    SLIGHT_DECREASE = -1
    MARKET_PRICE = 0
    SLIGHT_INCREASE = 1
    SIGNIFICANT_INCREASE = 2


class ShiftTime(Enum):
    NONE = 0
    H1 = 1
    H3 = 3
    H5 = 5
    H8 = 8


class ShiftAction(IAction):
    def __init__(self, shift_time: ShiftTime, price_level: PriceLevel):
        super().__init__()
        self._shift_time: ShiftTime = shift_time
        self._price_level: PriceLevel = price_level

    @override
    def execute(self, microgrid: "IMicrogrid", time_step: int) -> float:
        total_loads = sum(
            map(
                lambda load: load.shift(
                    shift_time=self._shift_time.value,
                    price_level=self._price_level.value,
                    current_time=time_step % 24,
                ),
                microgrid.residential_loads,
            )
        )
        return total_loads

    @classmethod
    @override
    def calc_action_space(cls) -> int:
        return len(PriceLevel) * len(ShiftTime)

    @classmethod
    @override
    def from_action_space(cls, action: int, **kwargs) -> ShiftAction:
        if action < 0 or action >= cls.calc_action_space():
            raise ValueError(f"Action ({action}) has to be in range [0, {cls.calc_action_space()})")
        price_levels = list(PriceLevel)
        shift_times = list(ShiftTime)

        price_idx = action // len(shift_times)
        shift_idx = action % len(shift_times)

        price_level = price_levels[price_idx]
        shift_time = shift_times[shift_idx]
        return cls(shift_time=shift_time, price_level=price_level)

    def get_price_level(self) -> PriceLevel:
        return self._price_level

    def get_shift_time(self) -> ShiftTime:
        return self._shift_time

    def __repr__(self):
        return f"ShiftAction({self._shift_time}, {self._price_level})"
