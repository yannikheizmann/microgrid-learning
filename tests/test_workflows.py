"""Short automated equivalents of the original manual evaluation workflows."""

import csv
from pathlib import Path

import numpy as np
import pytest
import torch
from stable_baselines3.common.callbacks import CallbackList

from rl_microgrid.config.configuration.args import Args
from rl_microgrid.config.factory import EnvironmentFactory
from rl_microgrid.main import Main


@pytest.mark.parametrize("microgrid,reward,extra", [("Basic", "Basic", 0), ("CarBattery", "CarBattery", 4)])
def test_observation_and_full_day(microgrid, reward, extra):
    env = EnvironmentFactory.create(Args(microgrid=microgrid, reward=reward))
    observation, _ = env.reset(seed=0)
    assert observation.shape == (5 + extra + len(env.microgrid.residential_loads),)
    assert observation.dtype == np.float32
    assert np.isfinite(observation).all()
    for step in range(24):
        observation, value, terminated, truncated, info = env.step(0)
        assert observation.shape == env.observation_space.shape
        assert np.isfinite(observation).all()
        assert np.isfinite(value)
        assert terminated == (step == 23)
        assert not truncated
        assert info["energy_bought"] >= 0
        assert info["energy_sold"] >= 0
    env.close()


def assert_evaluation(run_name):
    output = Path("data/testing/test_results")
    with (output / f"test_results_{run_name}.csv").open() as stream:
        rows = list(csv.DictReader(stream))
    assert len(rows) == 1
    row = rows[0]
    assert float(row["Net_Profit"]) == pytest.approx(float(row["Money_Earned"]) - float(row["Money_Spent"]))
    assert sum(int(row[f"Top_Action_{i}_Count"]) for i in range(1, 4)) <= 24
    assert (output / f"test_results_{run_name}.png").stat().st_size > 0


@pytest.mark.parametrize("agent_name", ["BaselineBatteryFirst", "BaselineGridFirst"])
def test_baseline_evaluation(agent_name):
    agent = Main.instantiate(Args(agent=agent_name))
    agent.test(n_episodes=1, input_model_path=None, run_name=agent_name)
    assert_evaluation(agent_name)


class OfflineTracker:
    def callbacks(self):
        return CallbackList([])


@pytest.mark.parametrize(
    "microgrid,reward", [("Basic", "Basic"), ("CarBattery", "CarBattery"), ("CarBattery", "Basic")]
)
def test_dqn_train_save_load_evaluate(tmp_path, microgrid, reward):
    """Exercise actual gradient updates and persistence, not convergence."""
    torch.manual_seed(42)
    args = Args(
        agent="SB3_DQN", microgrid=microgrid, reward=reward, batch_size=4, additional_agent_args={"memory_size": 32}
    )
    agent = Main.instantiate(args)
    assert agent._model.buffer_size == 32
    agent._model.learning_starts = 0
    before = [parameter.detach().clone() for parameter in agent._model.q_net.parameters()]
    agent.train(n_episodes=8, output_path=str(tmp_path), tracker=OfflineTracker())
    assert agent._model._n_updates > 0
    assert any(not torch.equal(old, new) for old, new in zip(before, agent._model.q_net.parameters()))
    model = tmp_path / "microgrid_model.pth"
    assert model.is_file()
    observation, _ = agent._environment.reset(seed=0)
    expected = agent._act(observation, deterministic=True)
    restored = Main.instantiate(args)
    restored._load_model(str(model))
    assert restored._act(observation, deterministic=True) == expected
    restored.test(n_episodes=1, input_model_path=str(model), run_name="restored")
    assert_evaluation("restored")
