▷ [**Usage-Guide**](#usage) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
☐ [**Structure-Guide**](./src/rl_microgrid/README.md#structure) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
⧉ [**Extension-Guide**](./src/rl_microgrid/README.md#extension) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 
⚙ [**Configuration-Guide**](./src/rl_microgrid/config/README.md#configuration) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
❖ [**Pattern-Guide**](./src/rl_microgrid/config/README.md#patterns) 
 
---

# RL Microgrid

Simulation of a Microgrid and Reinforcement Learning an Energy Model.

[UML](https://drive.google.com/file/d/1i6VEqIuQm0UATBUnb5yf2VMYq463seAv/view?usp=sharing)

## Installation

### Requirements

This project uses [`uv`](https://docs.astral.sh/uv/) to manage python versions and all dependencies.
For installation, follow the manual for your system [here](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer).  
`uv` will create and manage a `venv` according to the specifications given in [`pyproject.toml`](./pyproject.toml).

### Install

To create or update your python environment, run
```bash
  uv sync
```
This will create a `.venv` (if not already exists), resolve and install all missing dependencies and write changes to [`uv.lock`](./uv.lock) file.  
This ensures, that all libraries are compatible with each other and improves reproducibility along different installations.

<a id="usage"></a>

## ▷ Usage

### Run Tests

Please run tests before committing your changes:

```bash
  uv run pytest
```

### Start Learning
To start the application, use the following command:

```bash
    uv run rl-microgrid --mode train --episodes 500
```
For an overview on all the available application arguments to be set when calling the run command, refer to the [Args](./src/rl_microgrid/config/configuration/args/_args.py) class. Each key of this class represents one argument that can be passed to the command, including information on aliases for the argument name, descriptions of the respective argument, as well as the default value used if not set. The default values can be reviewed and set [here](./src/rl_microgrid/config/configuration/static/_defaults.py). The options for the arguments refering to interchangeable components of the application, for example the RL-Algorithm used or the reward function used, can be seen [here](./src/rl_microgrid/config/configuration/options/_options.py) and can be set via the respective string-value.    
<span style="color: grey; font-size: 11px;">(For more detailed information on the configuration of this framework, please refer to the [Configuration-Guide ▷](./src/rl_microgrid/config/README.md#configuration),    
for more detailed information on the overall structure of this framework and the extension of it, please refer to the respective [Structure- ▷](./src/rl_microgrid/README.md#structure) or [Extension-Guide ▷](./src/rl_microgrid/README.md#extension))</span>   

### Evaluate Training

Start Tensorboard to view your training runs:
```bash
    tensorboard --logdir=data/tracking/tensorboard
```

## Collaboration

### Managing Dependencies

To add or remove dependencies, use

```bash
    uv add library-name
    uv remove library-name
```

For further information, read this [Guide](https://docs.astral.sh/uv/guides/projects/#managing-dependencies).

### Pre-commit
`pre-commit` is a tool for improving collaboration by running scripts, tests or formatting before changes are actually committed to git.  
After running `uc sync` for the first time, you need to activate `pre-commit` by running
```bash
    pre-commit install
```
Make sure to activate the environment before running `pre-commit install`.  
If the command cannot be found, you may also need to restart your IDE or system, as it just got installed and is probably not directly available in your terminal.

## Authors and acknowledgment
Show your appreciation to those who have contributed to the project.

## License
This project is licensed under MIT.
