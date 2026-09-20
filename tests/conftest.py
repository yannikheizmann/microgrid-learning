"""Keep test runs offline and their generated artifacts out of the checkout."""

import os
from pathlib import Path
import random
import shutil

import numpy as np
import pytest

os.environ["WANDB_MODE"] = "disabled"
os.environ["MPLBACKEND"] = "Agg"
os.environ.setdefault("MPLCONFIGDIR", "/tmp/microgrid-learning-matplotlib")


@pytest.fixture(autouse=True)
def isolated_run(tmp_path, monkeypatch):
    source = Path(__file__).resolve().parents[1] / "data"
    shutil.copytree(source, tmp_path / "data", ignore=shutil.ignore_patterns("models", "tracking", "testing"))
    monkeypatch.chdir(tmp_path)
    random.seed(42)
    np.random.seed(42)
