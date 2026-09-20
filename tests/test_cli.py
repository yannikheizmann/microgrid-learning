import argparse
import sys

import pytest

from rl_microgrid.config.configuration.args import ArgsParser


@pytest.mark.parametrize(
    "input_flag,output_flag", [("--in", "--out"), ("-in", "-out"), ("--input_model_path", "--output_path")]
)
def test_model_path_flags(monkeypatch, input_flag, output_flag):
    monkeypatch.setattr(
        sys,
        "argv",
        ["rl-microgrid", "--mode", "test", input_flag, "model.zip", output_flag, "models", "--episodes", "1"],
    )
    args = ArgsParser.parse()
    assert args.input_model_path == "model.zip"
    assert args.output_path == "models"
    assert args.episodes == 1
    assert args.mode == "test"


def test_nested_args_dictionary():
    args = ArgsParser._create_args_from_namespace(argparse.Namespace(additional_agent_args={"gamma": 0.5}))
    assert args.additional_agent_args.gamma == 0.5


@pytest.mark.parametrize("agent", ["BaselineBatteryFirst", "BaselineGridFirst"])
def test_baseline_command(monkeypatch, agent):
    from rl_microgrid.main import Main
    from pathlib import Path

    monkeypatch.setattr(
        sys, "argv", ["rl-microgrid", "--mode", "test", "--agent", agent, "--episodes", "1", "--run_name", "cli"]
    )

    def unexpected_tracker(*args, **kwargs):
        pytest.fail("Evaluation should not initialize experiment tracking")

    monkeypatch.setattr("rl_microgrid.main.Tracker", unexpected_tracker)
    Main.run()
    assert Path("data/testing/test_results/test_results_cli.csv").is_file()
