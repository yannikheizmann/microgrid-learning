from numpy.typing import NDArray
import numpy as np


def load_csv_data(path: str, skip_header: int, scaling_factor: int) -> NDArray[np.float64]:
    csv_data: NDArray[np.float64] = (
        np.genfromtxt(
            path,
            delimiter=",",
            skip_header=skip_header,
            usecols=[-1],
        )
        / scaling_factor
    )
    return csv_data
