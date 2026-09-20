from pathlib import Path
from typing import Literal

from torch import nn

from ._static import MODELS_PATH
from ..options import AgentOptions, BrainOptions, MicrogridFactoryOptions, RewardOptions
from ....utils import find_latest_model

# - default application variables -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
## - components -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
AGENT: AgentOptions = AgentOptions.SB3_DQN
BRAIN: BrainOptions = BrainOptions.MLP
MICROGRID: MicrogridFactoryOptions = MicrogridFactoryOptions.Basic
REWARD: RewardOptions = RewardOptions.Basic

## - process -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
MODE: Literal["train", "test"] = "train"
EPISODES: int = 1000
RANDOM_SEED: int = 42
BATCH_SIZE: int = 32
LEARNING_RATE: float = 0.001

## - paths -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
INPUT_MODEL_PATH: Path = find_latest_model(MODELS_PATH, "microgrid_model.pth")

## - specific -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
### - agent - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#### - dqn ---------------------------------------------------------------------------------------------------------------------------------
EPSILON = 0.99
GAMMA: float = 0.99
MEMORY_SIZE: int = 10000

### - brain - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
HIDDEN_DIMS: list[int] = [128, 64]
ACTIVATION: str = nn.ReLU()
