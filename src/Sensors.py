import numpy as np
from abc import ABC, abstractmethod

class Sensor(ABC):
    def __init__(self, name: str, min_resolution: float):
        self.name = name
        self.min_resolution = min_resolution

    @abstractmethod
    def read_measurement(self, real_concentration: float) -> float:
        """
        Applies sensor-specific noise and resolution limits to the ground-truth value.
        """
        pass

class PIDGasSensor(Sensor):
    def __init__(self, name: str, min_resolution: float, noise_std: float = 0.001):
        super().__init__(name, min_resolution)
        self.noise_std = noise_std

    def read_measurement(self, real_concentration: float) -> float:
        noise = np.random.normal(0, self.noise_std)
        meas = real_concentration + noise

        # Applies minimum resolution threshold
        if meas < self.min_resolution:
            return 0.0
        return float(meas)