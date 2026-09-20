from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
import csv
from collections import Counter
import os

import numpy as np
import torch

from ..brains import IBrain
from ...config.registry import RegistryMeta
from ...environment import MicrogridEnvironment
from ...utils import MicrogridEnvironmentPlot

if TYPE_CHECKING:
    from ...utils.tracking import Tracker


class IAgent(ABC, metaclass=RegistryMeta["IAgent"]):
    def __init__(
        self,
        environment: MicrogridEnvironment,
        brain: IBrain,
        batch_size: int,
    ) -> None:
        self._environment = environment
        self._brain = brain
        self._batch_size = batch_size

    @abstractmethod
    def _load_model(self, model_path: str) -> None:
        pass

    @abstractmethod
    def _act(self, observation: np.ndarray, deterministic: bool = False):
        """Select an action based on the current state."""
        pass

    @abstractmethod
    def train(
        self,
        n_episodes: int,
        output_path: str,
        tracker: "Tracker",
        *args,
        **kwargs,
    ) -> None:
        pass

    def test(self, n_episodes: int, input_model_path: str, run_name: str = "default_run") -> None:
        """Test the trained DQN agent and record results in a CSV file.

        Args:
            n_episodes: Number of episodes to test
            input_model_path: Path to the trained model
            run_name: Name of the test run for identification
        """
        print("Starting testing")
        self._load_model(input_model_path)

        env_plot = MicrogridEnvironmentPlot(n_episodes)
        total_money_spent = 0
        total_money_earned = 0

        # Create results directory if it doesn't exist
        results_dir = "data/testing/test_results"
        os.makedirs(results_dir, exist_ok=True)

        # Create CSV file with run name
        csv_filename = os.path.join(results_dir, f"test_results_{run_name}.csv")

        with open(csv_filename, "w", newline="") as csvfile:
            fieldnames = [
                "Day",
                "Money_Spent",
                "Money_Earned",
                "Net_Profit",
                "Top_Action_1",
                "Top_Action_1_Count",
                "Top_Action_2",
                "Top_Action_2_Count",
                "Top_Action_3",
                "Top_Action_3_Count",
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for day in range(n_episodes):
                observation, info = self._environment.reset(seed=day)
                day_money_spent = 0
                day_money_earned = 0
                action_counter = Counter()

                terminal = False
                while not terminal:
                    with torch.no_grad():
                        action = self._act(observation, deterministic=True)
                        action_counter[action] += 1

                    next_observation, reward, terminal, _, info = self._environment.step(action)
                    observation = next_observation
                    env_plot.collect_info(info)

                    # Track money spent/earned
                    if info["energy_bought"] > 0:
                        day_money_spent += info["energy_bought"] * info["grid_buy_price"]
                    if info["energy_sold"] > 0:
                        day_money_earned += info["energy_sold"] * info["grid_sell_price"]

                total_money_spent += day_money_spent
                total_money_earned += day_money_earned

                # Get top 3 actions
                top_actions = action_counter.most_common(3)
                row_data = {
                    "Day": day + 1,
                    "Money_Spent": day_money_spent,
                    "Money_Earned": day_money_earned,
                    "Net_Profit": day_money_earned - day_money_spent,
                }

                # Add top 3 actions and their counts
                for i, (action, count) in enumerate(top_actions, 1):
                    row_data[f"Top_Action_{i}"] = action
                    row_data[f"Top_Action_{i}_Count"] = count

                # Fill in remaining top actions with None if less than 3
                for i in range(len(top_actions) + 1, 4):
                    row_data[f"Top_Action_{i}"] = None
                    row_data[f"Top_Action_{i}_Count"] = 0

                writer.writerow(row_data)

        print(f"\nTest results have been saved to {csv_filename}")
        print("\nOverall Summary:")
        print(f"Total money spent: {total_money_spent:.2f}")
        print(f"Total money earned: {total_money_earned:.2f}")
        print(f"Total net profit: {total_money_earned - total_money_spent:.2f}")

        env_plot.plot_to_file(os.path.join(results_dir, f"test_results_{run_name}.png"))
