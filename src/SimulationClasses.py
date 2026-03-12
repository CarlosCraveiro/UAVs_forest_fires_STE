from dataclasses import dataclass
from typing import Callable, Tuple
from MovementStrategies import MovementStrategy
from Sensors import Sensor

@dataclass
class DispersionModelConfig:
    """Armazena os parâmetros reais do ambiente (Ground Truth)."""
    source_position: Tuple[float, float, float]
    q: float
    u: float
    zetas: Tuple[float, float]
    wind_angles: Tuple[float, float]

class World:
    def __init__(self, dispersion_model: Callable, model_config: DispersionModelConfig):
        self.uav_positions = {}
        self.dispersion_model = dispersion_model
        self.model_config = model_config

    def register_uav(self, uav_id: str, initial_position: tuple):
        self.uav_positions[uav_id] = initial_position

    def get_real_position(self, uav_id: str):
        return self.uav_positions.get(uav_id)

    def set_real_position(self, uav_id: str, new_pos: tuple):
        self.uav_positions[uav_id] = new_pos

    def get_real_concentration(self, pos: tuple):
        """
        O World chama a função do modelo passando as configurações armazenadas.
        Se a configuração for alterada em tempo de execução, a concentração muda dinamicamente.
        """
        return self.dispersion_model(
            pos,
            self.model_config.source_position,
            self.model_config.q,
            self.model_config.u,
            self.model_config.zetas,
            self.model_config.wind_angles
        )

class UAV:
    def __init__(self, uav_id: str, world: World, strategy: MovementStrategy):
        self.id = uav_id
        self.world = world
        self.strategy = strategy
        self.sensors = {} # Dictionary to hold multiple sensors by name

    def add_sensor(self, sensor: Sensor):
        self.sensors[sensor.name] = sensor

    def get_sensor(self, name: str) -> Sensor:
        if name not in self.sensors:
            raise ValueError(f"Sensor '{name}' not found on UAV '{self.id}'")
        return self.sensors[name]

    def get_position(self):
        return self.world.get_real_position(self.id)

    def set_position(self, new_pos):
        self.world.set_real_position(self.id, new_pos)