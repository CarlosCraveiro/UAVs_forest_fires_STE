import numpy as np

def gaussian_plume_gp(sensor_pos, source_pos, qs, us, zetas, wind_euler):
    """
    Gaussian Plume (GP) model using Euler angles for wind direction.
    """
    X, Y, sensor_height = sensor_pos
    xs, ys, zs = source_pos
    zeta1, zeta2 = zetas

    pitch, yaw = wind_euler

    # Conversão de Ângulos de Euler (Pitch e Yaw) para Vetor Unitário 3D.
    # Assumindo a convenção em que Yaw é a rotação no plano XY e Pitch é a elevação.
    ux = np.cos(yaw) * np.cos(pitch)
    uy = np.sin(yaw) * np.cos(pitch)
    uz = np.sin(pitch)

    dx = X - xs
    dy = Y - ys
    dz = sensor_height - zs

    dk = dx * ux + dy * uy + dz * uz
    ck = -dx * uy + dy * ux

    r = np.sqrt(dx**2 + dy**2 + dz**2)
    r_safe = np.maximum(r, 1e-10)

    sigma_y = (zeta1 * r_safe) / np.sqrt(1 + 0.0001 * r_safe)
    sigma_z = (zeta2 * r_safe) / np.sqrt(1 + 0.0001 * r_safe)

    scale_term = qs / (us * sigma_y * sigma_z * 2 * np.pi)
    cross_term = np.exp(-(ck**2) / (2 * sigma_y**2))

    vert_term = np.exp(-(dz**2) / (2 * sigma_z**2)) + \
                np.exp(-((sensor_height + zs)**2) / (2 * sigma_z**2))

    concentration = scale_term * cross_term * vert_term
    concentration = np.where(dk > 0, concentration, 0.0)

    return concentration