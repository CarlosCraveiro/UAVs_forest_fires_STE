import numpy as np
from abc import ABC, abstractmethod

from typing import Any

class MovementStrategy(ABC):
    @abstractmethod
    def compute_next_step(self, t: Any = None, memory: Any = None) -> tuple:
        """
        Calcula o próximo passo. 
        'memory' pode conter as partículas ou o estado do estimador.
        """
        pass

class ParameterizedSweepStrategy(MovementStrategy):
    def __init__(self, x_max, y_max, num_sectors):
        self.x_max = x_max
        self.y_max = y_max
        self.num_sectors = num_sectors
        self.waypoints = []

        y_step = y_max / (num_sectors - 1) if num_sectors > 1 else 0
        for i in range(num_sectors):
            curr_y = i * y_step
            if i % 2 == 0:
                self.waypoints.append(np.array([0.0, curr_y]))
                self.waypoints.append(np.array([x_max, curr_y]))
            else:
                self.waypoints.append(np.array([x_max, curr_y]))
                self.waypoints.append(np.array([0.0, curr_y]))

        self.waypoints = np.array(self.waypoints)
        diffs = np.diff(self.waypoints, axis=0)
        segment_lengths = np.sqrt((diffs**2).sum(axis=1))
        self.cum_dist = np.concatenate(([0], np.cumsum(segment_lengths)))
        self.total_length = self.cum_dist[-1]
        self.normalized_dist = self.cum_dist / self.total_length

    def compute_next_step(self, t: float, memory: Any = None):
        t = np.clip(t, 0, 1)
        x = np.interp(t, self.normalized_dist, self.waypoints[:, 0])
        y = np.interp(t, self.normalized_dist, self.waypoints[:, 1])
        return (x, y, 2.5)