from typing import override

from ...microgrid.actions import CompositeResult
from ._base import IReward

from .. import MicrogridEnvironment


class CarBatteryReward(IReward):
    @classmethod
    @override
    def calculate_reward(
        cls,
        env: MicrogridEnvironment,
        action_result: CompositeResult,
    ) -> float:
        """
        Calculate a basic reward based on the microgrid state and action result.

        This basic reward function is mainly based on:
        - Positive reward for energy sold to the grid
        - Negative reward for energy bought from the grid
        - Negative reward for not achieving requested CarBattery SoC near target_time

        Args:
            env: The microgrid environment
            action_result: The result of the composite action

        Returns:
            The calculated reward as a float value
        """
        reward = 0.0
        reward -= env.microgrid.car_battery.needs_charging(env.microgrid.external_grid.current_time) * 0.1

        # Cost of energy produced from DER
        reward -= action_result.generated_energy * env.power_cost / 100

        # Increment reward by amount of return, based on the sale price
        sale_price = action_result.price_level.value + env.market_price
        reward += action_result.total_load * sale_price / 100

        # Add the money from selling or buying (negative) to reward
        reward += action_result.price / 100

        return reward
