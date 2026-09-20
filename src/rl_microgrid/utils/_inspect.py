from pathlib import Path
from datetime import datetime
from typing import Optional

from ..config.configuration.static import DATETIME_FORMAT


def find_latest_model(base_dir: Path, model_filename: str) -> Optional[str]:
    """
    Find the latest folder based on datetime-named folders containing a specific model file.

    Args:
        base_dir (Path): The base directory to search in.
        model_filename (str): The filename to check for inside each folder.

    Returns:
        Optional[Path]: Path to the model file in the latest valid folder, or None if none found.
    """
    candidates: list[tuple[datetime, Path]] = []
    for folder in base_dir.iterdir():
        if folder.is_dir() and (folder / model_filename).exists():
            try:
                folder_datetime = datetime.strptime(folder.name, DATETIME_FORMAT)
                candidates.append((folder_datetime, folder))
            except ValueError:
                continue
    if not candidates:
        return None
    latest_folder = max(candidates, key=lambda x: x[0])[1]
    return (latest_folder / model_filename).as_posix()
