import numpy as np
from typing import Any
from dataclasses import dataclass
from Estimators import SourceEstimator, EstimatorConfig

@dataclass
class ParticleFilterConfig(EstimatorConfig):
    num_particles: int
    n_eff_threshold: float
    resample_function: str
    target_sensor_name: str

class ParticleFilter(SourceEstimator):
    def __init__(self):
        # Substituímos 'phi' pelos três ângulos de Euler
        self.particle_dtype = np.dtype([
            ('weight', np.float64),
            ('x_s', np.float64),
            ('y_s', np.float64),
            ('q', np.float64),
            ('u_s', np.float64),
            ('roll', np.float64),
            ('pitch', np.float64),
            ('yaw', np.float64),
            ('zeta1', np.float64),
            ('zeta2', np.float64)
        ])

    def initialize_particles(self, config: ParticleFilterConfig, prior_params: dict) -> np.ndarray:
        """
        Inicializa o array estruturado de partículas amostrando das distribuições a priori.
        """
        N = config.num_particles
        
        particles = np.zeros(N, dtype=self.particle_dtype)
        
        particles['weight'] = 1.0 / N
        
        particles['x_s'] = np.random.uniform(prior_params["x_s"]["low"], prior_params["x_s"]["high"], N)
        particles['y_s'] = np.random.uniform(prior_params["y_s"]["low"], prior_params["y_s"]["high"], N)
        particles['q'] = np.random.gamma(prior_params["q"]["shape"], prior_params["q"]["scale"], N)
        particles['u_s'] = np.random.normal(prior_params["u_s"]["mean"], prior_params["u_s"]["std"], N)
        
        # Amostrando os ângulos de Euler
        particles['pitch'] = np.random.uniform(prior_params["pitch"]["low"], prior_params["pitch"]["high"], N)
        particles['yaw'] = np.random.uniform(prior_params["yaw"]["low"], prior_params["yaw"]["high"], N)
        
        particles['zeta1'] = np.random.uniform(prior_params["zeta1"]["low"], prior_params["zeta1"]["high"], N)
        particles['zeta2'] = np.random.uniform(prior_params["zeta2"]["low"], prior_params["zeta2"]["high"], N)
        
        return particles

    def step(self, uav_data: dict, memory: Any, config: EstimatorConfig) -> np.ndarray:
        """
        Executa um passo de estimação.
        """
        particles = memory
        
        # TODO: Predição (movimento aleatório das partículas)
        # TODO: Atualização (cálculo do likelihood usando o modelo de dispersão)
        # TODO: Normalização dos pesos
        # TODO: Reamostragem (se N_eff < threshold)
        
        return particles