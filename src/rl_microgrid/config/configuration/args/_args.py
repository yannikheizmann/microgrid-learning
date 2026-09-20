from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Any, Union, Callable, Optional
import inspect

from ..options import (
    AgentOptions,
    BrainOptions,
    MicrogridFactoryOptions,
    RewardOptions,
)
from ..static import (
    AGENT,
    BRAIN,
    MICROGRID,
    REWARD,
    MODE,
    INPUT_MODEL_PATH,
    OUTPUT_PATH,
    EPISODES,
    MEMORY_SIZE,
    BATCH_SIZE,
    GAMMA,
    LEARNING_RATE,
    HIDDEN_DIMS,
    EPSILON,
)


class IAdditionalArgs(BaseModel):
    pass


class AdditionalBrainArgs(IAdditionalArgs):
    hidden_dims: list[int] = Field(description="Comma-separated hidden layer dimensions", default=HIDDEN_DIMS)

    class Config:
        extra = "allow"


class AdditionalAgentArgs(IAdditionalArgs):
    memory_size: int = Field(description="Size of replay memory (for dqn)", default=MEMORY_SIZE)
    epsilon: float = Field(
        description="Epsilon for epsilon-greedy action selection (for dqn)",
        default=EPSILON,
    )
    gamma: float = Field(description="Discount factor for future rewards (for dqn)", default=GAMMA)
    exploration_initial_eps: float = Field(
        description="Initial epsilon value for exploration (1.0 = completely random)",
        default=1.0,
    )
    exploration_final_eps: float = Field(
        description="Final epsilon value for exploration (0.05 = almost deterministic)",
        default=0.05,
    )
    exploration_fraction: float = Field(
        description="Fraction of training after which epsilon reaches final value (0.3 = after 30% of training)",
        default=0.3,
    )
    target_update_interval: int = Field(
        description="Number of steps between target network updates (default: weekly)",
        default=24 * 7,
    )

    class Config:
        extra = "allow"


# TODO implement input checks with @model_validator(mode="after") method
class Args(BaseModel):
    agent: AgentOptions = Field(description="Agent to use", default=AGENT)
    brain: BrainOptions = Field(description="Brain to use", default=BRAIN)
    microgrid: MicrogridFactoryOptions = Field(description="Microgrid factory to use", default=MICROGRID)
    reward: RewardOptions = Field(description="Reward function to use", default=REWARD)
    mode: str = Field(
        description="Mode: 'train' to train, 'test' to test a trained agent",
        default=MODE,
        pattern="^(train|test)$",
    )
    input_model_path: Optional[str] = Field(
        alias="in", description="Path to the input model file", default=INPUT_MODEL_PATH
    )
    output_path: str = Field(
        alias="out",
        description="Path to the output model file",
        default=OUTPUT_PATH.as_posix(),
    )
    run_name: str = Field(description="Name of the test run for identification", default="default_run")
    episodes: int = Field(description="Number of episodes to train", default=EPISODES)
    batch_size: int = Field(description="Batch size for training", default=BATCH_SIZE)
    learning_rate: float = Field(alias="lr", description="Learning rate for the brain", default=LEARNING_RATE)
    additional_brain_args: AdditionalBrainArgs = Field(
        alias="aba",
        description="Arguments for configuring the brain",
        default_factory=AdditionalBrainArgs,
    )
    additional_agent_args: AdditionalAgentArgs = Field(
        alias="aaa",
        description="Arguments for configuring the agent",
        default_factory=AdditionalAgentArgs,
    )

    class Config:
        validate_by_name = True

    def _as_flattened_dict(self) -> dict[str, Any]:
        flattened_dict: dict[str, Any] = {}
        for key, value in self.model_dump().items():
            if isinstance(value, BaseModel):
                for nested_key, nested_value in value.model_dump().items():
                    if nested_key in flattened_dict:
                        raise ValueError(f"Duplicate key found: '{nested_key}'")
                    flattened_dict[nested_key] = nested_value
            elif isinstance(value, dict):
                for nested_key, nested_value in value.items():
                    if nested_key in flattened_dict:
                        raise ValueError(f"Duplicate key found: '{nested_key}'")
                    flattened_dict[nested_key] = nested_value
            else:
                if key in flattened_dict:
                    raise ValueError(f"Duplicate key found: '{key}'")
                flattened_dict[key] = value
        return flattened_dict

    def call(self, method_or_class: Union[Callable[..., Any], type], **kwargs) -> Any:
        if inspect.isclass(method_or_class):
            signature = inspect.signature(method_or_class.__init__)
        else:
            signature = inspect.signature(method_or_class)
        args = self._as_flattened_dict()
        method_params = signature.parameters
        filtered_args = {key: value for key, value in args.items() if key in method_params}
        filtered_args.update({key: value for key, value in kwargs.items() if key in method_params})
        return method_or_class(**filtered_args)

    def save(self) -> None:
        """
        Save the current Args instance as a JSON file to the specified output_model_path.
        """
        with open(f"{self.output_path}/args.json", "w") as f:
            f.write(self.model_dump_json(indent=4))
