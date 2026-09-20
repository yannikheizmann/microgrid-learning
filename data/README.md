# Simulation inputs

These inputs are preserved from the [original bachelor project](https://github.com/yaHzm/rlmicrogrid/tree/121cbf17646a0119f842eedc9336c2abcc18f5f3/data).

- `up_regulation.csv`: grid purchase prices (last column, divided by 10).
- `down_regulation.csv`: grid sale prices (last column, divided by 10).
- `wind_generation_fortum.csv`: wind generation (last column, divided by 100).

The component defaults load these files relative to the working directory, so run commands from the repository root. The original data files are retained without changing their values or units. Unused historical inputs and generated experiment results remain in the original repository.
