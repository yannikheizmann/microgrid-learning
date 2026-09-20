from abc import ABC, abstractmethod
import torch
from torch import nn
import numpy as np

from ...config.registry import RegistryMeta


class IBrain(ABC, metaclass=RegistryMeta["IBrain"]):
    def __init__(self, input_dim: int, output_dim: int, learning_rate: float):
        self._device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self._input_dim = input_dim
        self._output_dim = output_dim
        self._net = self._create()
        self._optimizer = torch.optim.Adam(self._net.parameters(), lr=learning_rate)

    def get_net(self) -> nn.Module:
        return self._net.to(self._device)

    @abstractmethod
    def _create(self) -> nn.Module:
        pass

    def predict(self, observations: list[np.ndarray]) -> list[np.ndarray]:
        self._net.eval()
        with torch.no_grad():
            tensor_obs = torch.tensor(np.array(observations), dtype=torch.float32, device=self._device)
            if tensor_obs.ndim == 1:
                tensor_obs = tensor_obs.unsqueeze(0)
            q_values = self._net(tensor_obs)
            return [values.cpu().numpy().squeeze() for values in q_values]

    def train(self, observations: list[np.ndarray], target_q_values: list[np.ndarray]) -> None:
        self._net.train()
        inputs = torch.tensor(np.array(observations), dtype=torch.float32, device=self._device)
        targets = torch.tensor(np.array(target_q_values), dtype=torch.float32, device=self._device)

        predictions = self._net(inputs)
        loss = nn.MSELoss()(predictions, targets)

        self._optimizer.zero_grad()
        loss.backward()
        self._optimizer.step()
