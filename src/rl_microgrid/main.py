from __future__ import annotations
import numpy as np
import torch
import random

from rl_microgrid.config.configuration.static import RANDOM_SEED, PROJECT_NAME
from rl_microgrid.config.configuration.args import Args, ArgsParser
from rl_microgrid.config.factory import AgentFactory, EnvironmentFactory
from rl_microgrid.reinforcement_learning.agents import IAgent
from rl_microgrid.utils.tracking import Tracker


# TODO set up logging

# Set random seeds for reproducibility
np.random.seed(RANDOM_SEED)
torch.manual_seed(RANDOM_SEED)
random.seed(RANDOM_SEED)


class Main:
    @classmethod
    def instantiate(cls, args: Args) -> IAgent:
        environment = EnvironmentFactory.create(args=args)
        agent = AgentFactory.create(
            environment=environment,
            args=args,
        )
        return agent

    @classmethod
    def run(cls) -> None:
        args = ArgsParser.parse()
        agent = cls.instantiate(args)
        if args.mode == "train":
            tracker = Tracker(PROJECT_NAME, args)
            try:
                args.call(
                    agent.train,
                    n_episodes=args.episodes,
                    output_path=args.output_path,
                    tracker=tracker,
                )
                args.save()
            finally:
                tracker.finish()
        else:
            args.call(
                agent.test,
                n_episodes=args.episodes,
                input_model_path=args.input_model_path,
                run_name=args.run_name,
            )


if __name__ == "__main__":
    Main.run()
