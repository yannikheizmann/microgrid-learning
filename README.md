# Microgrid Learning

A Python framework for simulating a microgrid and training reinforcement learning agents to control battery storage, electricity purchases, and energy sales. It includes a Gymnasium environment, configurable components and rewards, rule-based baselines, and custom and Stable-Baselines3 DQN agents.

This is a cleaned continuation of our [original bachelor project, RL Microgrid](https://github.com/yaHzm/rlmicrogrid), imported from commit `121cbf17646a0119f842eedc9336c2abcc18f5f3`. The original repository preserves the project history, diagrams, legacy implementation, and experiment results.

## Setup

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then run these commands from the repository root. Python 3.12 is required; uv can install it automatically.

```bash
uv sync --locked
uv run pytest
```

The Python package and command retain the name `rl-microgrid` for compatibility. Runtime data is read from `data/` relative to the working directory.

## Run a baseline

```bash
uv run rl-microgrid --mode test --agent BaselineBatteryFirst --episodes 1 --run_name battery_first
uv run rl-microgrid --mode test --agent BaselineGridFirst --episodes 1 --run_name grid_first
```

Evaluation writes CSV summaries and plots to `data/testing/test_results/`. Use a unique run name to preserve earlier results.

## Train and evaluate

For local training without a Weights & Biases account:

```bash
WANDB_MODE=disabled uv run rl-microgrid --agent SB3_DQN --microgrid Basic --reward Basic --mode train --episodes 10000 --out data/models/basic
uv run rl-microgrid --agent SB3_DQN --microgrid Basic --reward Basic --mode test --episodes 10 --in data/models/basic/microgrid_model.pth --run_name basic
```

For a microgrid with an electric vehicle battery, use `--microgrid CarBattery --reward CarBattery` for both commands. Keep the training and evaluation configurations consistent. SB3 stores its model as `microgrid_model.pth`.

For SB3 training, the existing `--episodes` argument means **environment timesteps**. During evaluation it means **simulated days**, each containing 24 steps. The custom DQN agent uses episodes during training.

Training uses Weights & Biases unless `WANDB_MODE=disabled` is set. TensorBoard logs can be viewed with:

```bash
uv run tensorboard --logdir data/tracking/tensorboard
uv run rl-microgrid --help
```

## Tests

`uv run pytest` runs offline checks for action encoding and priorities, battery shortfall purchases, observations and daily rollouts, baseline evaluation, CLI arguments, and short DQN training/save/load/evaluation workflows for both microgrid configurations. It also covers the historical CarBattery/Basic reward combination for compatibility; that combination is not a recommended training setup.

Tests use temporary output directories and include actual gradient updates. They validate execution and persistence, not policy convergence or reproduction of the original experimental results. Full training remains a separate experiment.

## Extend the framework

- [Architecture and extension guide](src/rl_microgrid/README.md)
- [Configuration and component patterns](src/rl_microgrid/config/README.md)
- [CLI argument definitions](src/rl_microgrid/config/configuration/args/_args.py)
- [Component defaults](src/rl_microgrid/config/configuration/microgrid/_microgrid.py)
- [Input datasets](data/README.md)

Agents, rewards, brains, and microgrid factories are selected through the registry and configuration options. The source guides retain links to diagrams in the original repository.

## Credits

Originally developed by Bennet Märtin, Joshua Ruf, Markus Portugall, Nick Abermeth, and Yannik Heizmann as a bachelor project. Author metadata is preserved in `pyproject.toml`.

The original README stated MIT licensing, but the imported snapshot contained no LICENSE file. This cleanup does not introduce a new license grant.
