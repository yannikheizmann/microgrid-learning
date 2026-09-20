from pydantic import Field
from numpy.typing import NDArray
import numpy as np
import random

from . import IConfig
from ..static import DATA_PATH
from ....utils import load_csv_data


# -- MICROGRID -----------------------------------------------------------------------
class MicrogridConfig(IConfig):
    """
    **A class representing the configuration arguments for a microgrid.**
    This class holds the configuration parameters required to define the behavior of a microgrid,
    including the number of distributed energy resources (DER) and residential loads.
    These parameters are used to initialize and manage a `Microgrid` object.

    Attributes:
        NUM_LOADS (int): Number of residential loads in the microgrid.
    """

    NUM_LOADS: int = Field(
        150,
        description="Number of residential loads in the microgrid.",
    )


# -- COMPONENTS ----------------------------------------------------------------------
# -- Battery -------------------------------------------------------------------------
class BatteryConfig(IConfig):
    """
    **A class representing the configuration arguments for a battery.**

    This class holds the configuration parameters required to define the behavior of a battery system,
    including its capacity, discharge efficiency, charging rate, and maximum energy input/output.
    These parameters are used to initialize and manage a `Battery` object.

    Attributes:
        CAPACITY (int): Total battery capacity in kWh.
        DISCHARGE_COEFFICIENT (float): Battery discharge efficiency coefficient.
        DISSIPATION_COEFFICIENT (float): Battery energy dissipation, i.e. energy lost over time.
        CHARGING_RATE (float): Maximum battery charging rate as proportion of its total capacity per charging cycle.
        MAX_DISCHARGE (int): Maximum allowable discharge rate in kW.
        MAX_ENERGY_INPUT (int): Maximum energy input per charging cycle in kWh.
    """

    CAPACITY: int = Field(500, description="Total battery capacity in kWh.")
    DISCHARGE_COEFFICIENT: float = Field(0.9, description="Battery discharge efficiency coefficient.")
    DISSIPATION_COEFFICIENT: float = Field(0.01, description="Battery energy dissipation, i.e. energy lost over time.")
    CHARGING_RATE: float = Field(
        0.9,
        description="Maximum battery charging rate as proportion of its total capacity per charging cycle.",
    )
    MAX_DISCHARGE: int = Field(250, description="Maximum allowable discharge rate in kW.")
    MAX_ENERGY_INPUT: int = Field(250, description="Maximum energy input per charging cycle in kWh.")


# -- ExternalGrid --------------------------------------------------------------------
class ExternalGridConfig(IConfig):
    """
    **A class representing the configuration arguments for the external grid.**

    This class holds the configuration parameters required to define the behavior of an external grid,
    including sell prices, buy prices, and export/import fees.
    These parameters are used to initialize and manage an `ExternalGrid` object.

    Attributes:
        SELL_PRICES (NDArray[np.float64]): Array of sell prices (in cents per kWh) for exporting energy to the grid.
        BUY_PRICES (NDArray[np.float64]): Array of buy prices (in cents per kWh) for importing energy from the grid.
        EXPORT_FEES (float): Fees (in cents per kWh) charged for exporting energy to the grid.
        IMPORT_FEES (float): Fees (in cents per kWh) charged for importing energy from the grid.
    """

    SELL_PRICES: NDArray[np.float64] = Field(
        load_csv_data(DATA_PATH / "down_regulation.csv", 1, 10),
        description="Array of sell prices (in cents per kWh) for exporting energy to the grid.",
    )
    BUY_PRICES: NDArray[np.float64] = Field(
        load_csv_data(DATA_PATH / "up_regulation.csv", 1, 10),
        description="Array of buy prices (in cents per kWh) for importing energy from the grid.",
    )
    EXPORT_FEES: float = Field(
        0.09,
        description="Fees (in cents per kWh) charged for exporting energy to the grid.",
    )
    IMPORT_FEES: float = Field(
        0.97,
        description="Fees (in cents per kWh) charged for importing energy from the grid.",
    )


# -- DER -----------------------------------------------------------------------------
class DERConfig(IConfig):
    """
    **A class representing the configuration arguments for distributed energy resources (DER).**

    This class holds the configuration parameters required to define the behavior of distributed energy resources,
    such as wind or solar power generation. These parameters are used to initialize and manage a `DistributedEnergyResources` object.

    Attributes:
        POWER_GENERATED (NDArray[np.float64]): Array of power generation values (in kW) for the distributed energy resource.
    """

    POWER_GENERATED: NDArray[np.float64] = Field(
        load_csv_data(DATA_PATH / "wind_generation_fortum.csv", 0, 100),
        description="Array of power generation values (in kW) for the distributed energy resource.",
    )


# -- ResidentialLoad -----------------------------------------------------------------
# TODO: Potentially reintroduce parameters like patience, max variable load from price action to shift action
class ResidentialLoadConfig(IConfig):
    """
    **A class representing the configuration arguments for a residential load.**

    This class holds the configuration parameters required to define the behavior of a residential load,
    including price sensitivity, base load, maximum variable load, and patience. These parameters are used to
    initialize and manage a `ResidentialLoad` object.

    Attributes:
        PRICE_SENSITIVITY (float): The sensitivity of the load to price changes.
        BASE_LOAD (NDArray[np.float64]): Array representing the base load (in kW) of the residential load over a day.
        MAX_VARIABLE_LOAD (float): The maximum variable load (in kW) of the residential load.
        PATIENCE (int): The patience of the load, representing the number of timesteps it is willing to wait.
    """

    SENSITIVITY: float = Field(
        default_factory=lambda: random.normalvariate(0.4, 0.3),
        description="The sensitivity of the load to price changes.",
    )
    BASE_LOAD: NDArray[np.float64] = Field(
        np.array(
            [
                0.4,
                0.3,
                0.2,
                0.2,
                0.2,
                0.2,
                0.3,
                0.5,
                0.6,
                0.6,
                0.5,
                0.5,
                0.5,
                0.4,
                0.4,
                0.6,
                0.8,
                1.4,
                1.2,
                0.9,
                0.8,
                0.6,
                0.5,
                0.4,
            ]
        ),
        description="Array representing the base load (in kW) of the residential load over a day.",
    )
    PATIENCE: int = Field(
        # TODO: confusing Number creates a strange distribution with 10 as the mean and 6 as the std in both directions
        default_factory=lambda: int(random.normalvariate(10, 6)),
        description="The patience of the load, representing the number of timesteps it is willing to wait.",
    )


class CarBatteryConfig(IConfig):
    """
    **A class representing the configuration arguments for a car battery(EV).**

    This class holds the configuration parameters required to define the behavior of a car battery system,
    including its capacity, discharge efficiency, charging rate, and maximum energy input/output.
    These parameters are used to initialize and manage a `CarBattery` object.

    Attributes:
        CAPACITY (int): Total battery capacity in kWh.
        DISCHARGE_COEFFICIENT (float): Battery discharge efficiency coefficient.
        DISSIPATION_COEFFICIENT (float): Battery energy dissipation, i.e. energy lost over time.
        CHARGING_RATE (float): Maximum battery charging rate as proportion of its total capacity per charging cycle.
        MAX_DISCHARGE (int): Maximum allowable discharge rate in kW.
        MAX_ENERGY_INPUT (int): Maximum energy input per charging cycle in kWh.
    """

    CAPACITY: int = Field(500, description="Total battery capacity in kWh.")
    DISCHARGE_COEFFICIENT: float = Field(0.9, description="Battery discharge efficiency coefficient.")
    DISSIPATION_COEFFICIENT: float = Field(0.01, description="Battery energy dissipation, i.e. energy lost over time.")
    CHARGING_RATE: float = Field(
        0.9,
        description="Maximum battery charging rate as proportion of its total capacity per charging cycle.",
    )
    MAX_DISCHARGE: int = Field(250, description="Maximum allowable discharge rate in kW.")
    MAX_ENERGY_INPUT: int = Field(250, description="Maximum energy input per charging cycle in kWh.")
    DESIRED_SOC: float = Field(
        random.randint(5, 10) / 10,
        description="Desired State of Charge for the Battery",
    )
    TARGET_TIME: int = Field(
        random.randint(6, 14),
        description="Time of day (Iterations) when the SoC of the car battery should reach or exceed the desired SoC",
    )
    TIME_AWAY: int = Field(10, description="Amount of time is not available after the TargetTime")
