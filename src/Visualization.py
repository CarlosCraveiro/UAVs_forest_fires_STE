import numpy as np
import matplotlib.pyplot as plt

def plot_particle_filter_step(particles, trajectory, grid_x, grid_y, Z, source_pos, step, pause_time=0.05):
    """
    Visualiza a distribuição das partículas em 2D sobreposta à pluma real e à trajetória.
    """
    plt.clf() # Limpa o frame anterior para criar a animação

    # Background Plume (Ground Truth)
    if Z is not None:
        plt.contourf(grid_x, grid_y, Z, levels=50, cmap='jet', alpha=0.3)

    # Trajetória do UAV
    if trajectory:
        traj_pts = np.array(trajectory)
        plt.plot(traj_pts[:, 0], traj_pts[:, 1], 'w--', alpha=0.8, label='Trajetória')
        # Destaca a posição atual do drone
        plt.scatter(traj_pts[-1, 0], traj_pts[-1, 1], color='cyan', marker='^', s=150, edgecolors='black', label='UAV')

    # Partículas
    # Ordenamos pelas partículas de maior peso para que sejam desenhadas por cima
    order = np.argsort(particles['weight'])
    ordered_particles = particles[order]
    
    scatter = plt.scatter(
        ordered_particles['x_s'], ordered_particles['y_s'],
        c=ordered_particles['weight'], cmap='viridis',
        s=15, alpha=0.8, label='Partículas'
    )
    plt.colorbar(scatter, label='Peso da Partícula')

    # Posição Real da Fonte
    plt.scatter(source_pos[0], source_pos[1], color='red', marker='X', s=150, label='Fonte Real')

    plt.title(f"Filtro de Partículas - Iteração {step}")
    plt.xlabel("X [m]")
    plt.ylabel("Y [m]")
    plt.xlim(0, 50) 
    plt.ylim(0, 50)
    plt.legend(loc='upper right')
    plt.grid(True, linestyle=':', alpha=0.6)

    plt.pause(pause_time) # Atualiza a tela e devolve o controle para o loop principal

def plot_mission_results(grid_x, grid_y, Z, traj_history, meas_history, source_pos, wind_angles):
    plt.figure(figsize=(10, 8))

    # Background Plume
    heatmap = plt.contourf(grid_x, grid_y, Z, levels=100, cmap='jet', alpha=0.5)
    plt.colorbar(heatmap, label=r'Concentration $(g/m^3)$')

    # Trajectory
    traj_pts = np.array(traj_history)
    plt.plot(traj_pts[:, 0], traj_pts[:, 1], 'w--', alpha=0.7, label='UAV Path')

    # Measurements
    sizes = np.array(meas_history) * 5000 + 10
    plt.scatter(traj_pts[:, 0], traj_pts[:, 1], s=sizes, c='white',
                edgecolors='black', alpha=0.8, label='Measurements')

    # Conversão dos Ângulos para Projeção do Vetor 2D (Plano XY)
    pitch, yaw = wind_angles
    u_x = np.cos(yaw) * np.cos(pitch)
    u_y = np.sin(yaw) * np.cos(pitch)

    # Source and Wind
    plt.scatter(source_pos[0], source_pos[1], color='red', marker='X', s=100, label='Source')
    # Usando u_x e u_y para desenhar a seta de direção
    plt.quiver(source_pos[0], source_pos[1], u_x, u_y, color='black', scale=10, label='Wind Direction')

    plt.title("UAV Mission Simulation")
    plt.xlabel("X [m]")
    plt.ylabel("Y [m]")
    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.show()