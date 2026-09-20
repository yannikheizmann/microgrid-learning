from torch import nn
from typing import override

from ._base import IBrain
from ...config.configuration.static import HIDDEN_DIMS, ACTIVATION


class MLPBrain(IBrain):
    def __init__(
        self,
        input_dim: int,
        output_dim: int,
        learning_rate: float,
        hidden_dims: list[int] = HIDDEN_DIMS,
        activation: nn.Module = ACTIVATION,
    ) -> None:
        self._hidden_dims = hidden_dims
        self._activation = activation
        super().__init__(input_dim, output_dim, learning_rate)

    @override
    def _create(self) -> nn.Module:
        layers = []
        prev_dim = self._input_dim
        for hidden_dim in self._hidden_dims:
            layers.append(nn.Linear(prev_dim, hidden_dim))
            layers.append(self._activation)
            prev_dim = hidden_dim
        layers.append(nn.Linear(prev_dim, self._output_dim))
        return nn.Sequential(*layers)
