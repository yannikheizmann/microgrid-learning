import numpy as np

from ...config.configuration.microgrid import DERConfig


class DistributedEnergyResources:
    def __init__(self, der_config: DERConfig):
        self._power_generated = der_config.POWER_GENERATED

    def current_generation(self, time: int) -> int:
        return self._power_generated[time]

    def getCurrentGeneration(self, day, iteration, time):
        """Returns a Numpy-array filled with the attributes of the class"""
        current_generation = self.current_generation(time)
        generation_last_day = self._power_generated[day * iteration : day * iteration + iteration]
        # Normalize current generation over the last day
        current_generation = (current_generation - np.average(generation_last_day)) / np.std(generation_last_day)
        return current_generation
