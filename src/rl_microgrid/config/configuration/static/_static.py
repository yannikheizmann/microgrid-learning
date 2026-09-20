from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# We can't use ':' in windows paths
DATETIME_FORMAT = "%Y.%m.%d-%H%M%S"

# paths
DATA_PATH = Path("./data")
MODELS_PATH = DATA_PATH / "models"
OUTPUT_PATH: Path = MODELS_PATH / f"{datetime.now().strftime(DATETIME_FORMAT)}"
TRACKING_PATH = DATA_PATH / "tracking"
TENSORBOARD_PATH = TRACKING_PATH / "tensorboard"
load_dotenv()

# Create paths if they don't exist
DATA_PATH.mkdir(parents=True, exist_ok=True)
MODELS_PATH.mkdir(parents=True, exist_ok=True)
OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
TRACKING_PATH.mkdir(parents=True, exist_ok=True)
TENSORBOARD_PATH.mkdir(parents=True, exist_ok=True)
