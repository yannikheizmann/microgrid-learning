from __future__ import annotations
import random
from collections import deque
import pickle
import matplotlib.pyplot as plt
import time
import numpy as np
from pydantic import BaseModel, ConfigDict
import torch
from typing import override, TYPE_CHECKING
import os

from ....environment import MicrogridEnvironment
from .._base import IAgent
from ....reinforcement_learning.brains import IBrain

if TYPE_CHECKING:
    from ....utils.tracking import Tracker


class Sample(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    observation: np.ndarray
    action: int
    reward: float
    next_observation: np.ndarray


class Prediction(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    sample: Sample
    q_value: np.ndarray
    next_q_value: np.ndarray

    @staticmethod
    def from_arrays(
        batch: list[Sample], q_values: list[np.ndarray], next_q_values: list[np.ndarray]
    ) -> list[Prediction]:
        return [
            Prediction(sample=sample, q_value=q_value, next_q_value=next_q_value)
            for sample, q_value, next_q_value in zip(batch, q_values, next_q_values)
        ]


class Memory:
    def __init__(self, capacity: int) -> None:
        self._capacity = capacity
        self._samples = deque(maxlen=capacity)

    def add(self, sample: Sample):
        self._samples.append(sample)

    def sample(self, batch_size: int) -> list[Sample]:
        n = min(batch_size, len(self._samples))
        return random.sample(self._samples, n)


# https://stable-baselines3.readthedocs.io/en/master/modules/dqn.html#dqn-policies
# https://stable-baselines3.readthedocs.io/en/master/modules/dqn.html#example


class DQNAgent(IAgent):
    def __init__(
        self,
        environment: MicrogridEnvironment,
        brain: IBrain,
        batch_size: int,
        gamma: float,
        epsilon: float,
        memory_size: int,
    ):
        super().__init__(environment, brain, batch_size)
        self._memory = Memory(memory_size)
        self._deterministic = False
        self._epsilon = epsilon
        self._gamma = gamma

        self._observation_dim = environment.get_observation_dim()
        self._action_dim = environment.get_action_dim()

    # TODO
    @override
    def _load_model(self, model_path: str) -> None:
        pass

    @override
    def _act(self, observation: np.ndarray, deterministic: bool = False) -> int:
        # If deterministic or below exploration threshold, choose the greedy action
        if deterministic or random.random() > self._epsilon:
            return np.argmax(self._brain.predict(observation))

        # Otherwise, explore by choosing a random action
        self._epsilon *= 0.9999  # Decay epsilon
        return random.randint(0, self._action_dim - 1)

    @override
    def train(
        self,
        n_episodes: int,
        output_path: str,
        tracker: "Tracker",
        *args,
        **kwargs,
    ) -> None:
        callback = tracker.callbacks()

        print("Starting training")
        start_time = time.time()

        callback.on_training_start(locals(), globals())

        rewards = []
        episode_lengths = []

        for episode in range(n_episodes):
            observation, info = self._environment.reset()

            episode_reward = 0
            terminal = False
            step_count = 0

            while not terminal:
                action = self._act(observation)
                next_observation, reward, terminal, _, info = self._environment.step(action)
                callback.on_step()

                self._process_sample(observation, action, reward, next_observation)

                self._learn()

                observation = next_observation
                episode_reward += reward
                step_count += 1

            rewards.append(episode_reward)
            episode_lengths.append(step_count)

            # Tracker.log(
            #     {
            #         "episode_reward": episode_reward,
            #         "episode_length": step_count,
            #         "episode": episode + 1,
            #     }
            # )

            if (episode + 1) % 10 == 0:
                avg_reward = np.mean(rewards[-10:])
                avg_length = np.mean(episode_lengths[-10:])
                print(f"Episode {episode + 1}/{n_episodes}, Avg Reward: {avg_reward:.2f}, Avg Length: {avg_length:.1f}")

        callback.on_training_end()

        output_model_path = f"{output_path}/microgrid_model.pth"
        os.makedirs(os.path.dirname(output_model_path), exist_ok=True)
        torch.save(self._brain.get_net().state_dict(), output_model_path)
        print(f"Model saved to {output_model_path}")

        rewards_file = output_model_path.replace(".pth", "_rewards.pkl")
        with open(rewards_file, "wb") as f:
            pickle.dump(rewards, f)

        # Plot rewards
        plt.figure(figsize=(10, 5))
        plt.plot(rewards)
        plt.title("Training Rewards")
        plt.xlabel("Episode")
        plt.ylabel("Reward")
        plt.savefig(output_model_path.replace(".pth", "_rewards.png"))

        training_time = time.time() - start_time
        print(f"Training completed in {training_time:.2f} seconds")

    def _process_sample(
        self,
        observation: np.ndarray,
        action: int,
        reward: float,
        next_observation: np.ndarray,
    ) -> None:
        observation = Sample(
            observation=observation,
            action=action,
            reward=reward,
            next_observation=next_observation,
        )
        self._memory.add(observation)

    def _extract_observations(self, batch: list[Sample]) -> tuple[list[np.ndarray], list[np.ndarray]]:
        zero_observation = np.zeros(self._observation_dim)
        current_observations = [sample.observation for sample in batch]
        next_observations = [
            zero_observation if sample.next_observation is None else sample.next_observation for sample in batch
        ]
        return current_observations, next_observations

    def _get_predicted_q_values(
        self,
        current_observations: list[np.ndarray],
        next_observations: list[np.ndarray],
    ) -> tuple[list[np.ndarray], list[np.ndarray]]:
        # predict q values for current states
        q_values = self._brain.predict(current_observations)
        # predict q values for next states
        next_q_values = self._brain.predict(next_observations)
        return q_values, next_q_values

    def _predict(self, batch: list[Sample]) -> list[Prediction]:
        # extract the observations from the batch of samples
        current_observations, next_observations = self._extract_observations(batch)
        # get the predicted q values for the batch of current and next states
        q_values, next_q_values = self._get_predicted_q_values(current_observations, next_observations)
        # create predictions containing the qvalues and observations
        predictions = Prediction.from_arrays(batch, q_values, next_q_values)
        return predictions

    def _create_input(self, predictions: list[Prediction]) -> tuple[list[np.ndarray], list[np.ndarray]]:
        # get batch size (could differ from self._batch_size if memory.size < batch_size)
        batch_size = len(predictions)
        # instantiate empty observations array and target q values array
        observations = [np.zeros(self._observation_dim) for _ in range(batch_size)]
        target_q_values = [np.zeros(self._action_dim) for _ in range(batch_size)]
        # set target q values
        for i, prediction in enumerate(predictions):
            sample = prediction.sample
            target_q_value = prediction.q_value.copy()
            if sample.next_observation is None:
                target_q_value[sample.action] = sample.reward
            else:
                target_q_value[sample.action] = sample.reward + self._gamma * np.amax(prediction.next_q_value)
            observations[i] = sample.observation
            target_q_values[i] = target_q_value
        return observations, target_q_values

    def _learn(self) -> None:
        # sample a batch from the memory to train the brain with
        batch = self._memory.sample(self._batch_size)
        # get the predicted q values for the batch
        predictions = self._predict(batch)
        # create input observations and labels to train the brain with
        input_observations, target_q_values = self._create_input(predictions)
        # train the brain with the input observations and target q values
        self._brain.train(input_observations, target_q_values)
