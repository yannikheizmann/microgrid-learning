from ._base import IOptions


class AgentOptions(IOptions):
    """
    Enum for the available agents.
    """

    DQN = "DQN"
    SB3_DQN = "SB3_DQN"
    BASELINE_GRID_FIRST = "BaselineGridFirst"
    BASELINE_BATTERY_FIRST = "BaselineBatteryFirst"


class BrainOptions(IOptions):
    """
    Enum for the available brains.
    """

    MLP = "MLP"


class RewardOptions(IOptions):
    """
    Enum for the available reward functions.
    """

    Basic = "Basic"
    CarBattery = "CarBattery"


class MicrogridFactoryOptions(IOptions):
    """
    Enum for the available microgrid factories.
    """

    Basic = "Basic"
    CarBattery = "CarBattery"
