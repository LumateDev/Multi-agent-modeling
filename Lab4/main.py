import numpy as np
import matplotlib.pyplot as plt


def calculate_target_state(t, t_stop):
    mid = t_stop / 2
    return 0 if 0 <= t <= mid else 1


def calculate_agent_activity(k, target_state, previous_state):
    return k * (target_state - previous_state)


def state_through_interpolate(all_time, all_states, t_minus_tau):
    if t_minus_tau <= all_time[0]:
        return all_states[0]
    return np.interp(t_minus_tau, all_time, all_states)


def get_current_state(environment_T1, environment_T2, environment_D, previous_state, previous_state_2, delta_t,
                      current_control):
    return (
            (2 * environment_T2 * previous_state) -
            (environment_T2 * previous_state_2) +
            (environment_T1 * delta_t * previous_state) +
            (environment_D * (delta_t ** 2) * current_control) +
            (delta_t ** 2)
    ) / (environment_T2 + (environment_T1 * delta_t) + delta_t ** 2)


def is_converged(target_state, current_state, threshold=1):
    return abs(target_state - current_state)


def simulation(t, delta_t, t_stop, tau, k, t1, environment_T2, environment_D):
    all_time = [0]
    all_target_states = [0]
    all_states = [0, 0]
    all_stability = [0]

    while t < t_stop:
        all_time.append(t)

        current_target_state = calculate_target_state(t, t_stop)
        all_target_states.append(current_target_state)

        current_state_minus_tau = state_through_interpolate(all_time, all_states, float(t) - float(tau))
        current_control = calculate_agent_activity(k, current_target_state, current_state_minus_tau)
        current_state = get_current_state(t1, environment_T2, environment_D, all_states[-1], all_states[-2], delta_t,
                                          current_control)
        all_states.append(current_state)
        current_stability = is_converged(current_target_state, current_state)
        all_stability.append(current_stability)

        # Принты для отслеживания состояния
        # print(f"t: {t:.2f}, Target State: {current_target_state}, Current State: {current_state:.4f}, Stability: {current_stability}")

        t += delta_t

    return all_time, all_target_states, all_states, all_stability


def param_sweep(tau_range, k_range, t, delta_t, t_stop, t1_range, t2_range, d_range):
    best_params = None
    best_error = float('inf')

    best_tau, best_k, best_t1, best_t2, best_d = [], [], [], [], []

    for tau in tau_range:
        for k in k_range:
            for t1 in t1_range:
                for t2 in t2_range:
                    for d in d_range:

                        all_time, all_target_states, all_states, all_stability = simulation(t, delta_t, t_stop, tau, k,
                                                                                            t1, t2, d)
                        final_error = np.mean(all_stability)

                        # Принт для отслеживания ошибок
                        # print(f"Testing tau: {tau:.4f}, k: {k:.4f}, Final Error: {final_error:.4f}")

                        if final_error < best_error:
                            best_error = final_error
                            best_params = (tau, k, t1, t2, d)
                        best_tau.append(tau)
                        best_k.append(k)
                        best_t1.append(t1)
                        best_t2.append(t2)
                        best_d.append(d)

    return best_params, best_tau, best_k, best_t1, best_t2, best_d


def plot_results(best_tau, best_k, best_t1, best_t2, best_d, all_stability):
    # Построение поверхности tau, k
    tau_grid, param_gird = np.meshgrid(best_tau[:,0,0,0,0], best_k[0,:,0,0,0])
    errors = all_stability[:,:,0,0,0]
    figure = plt.figure(figsize=(10, 6))
    ax = figure.add_subplot(111, projection='3d')
    surf = ax.plot_surface(tau_grid, param_gird, errors, cmap='viridis')
    ax.set_xlabel('Tau')
    ax.set_ylabel('k')
    ax.set_zlabel('Error')
    figure.colorbar(surf, ax=ax, label='Error')
    plt.title('Зависимость ошибки от параметров tau и k')
    plt.show()

    # Построение поверхности tau, t1
    tau_grid, param_gird = np.meshgrid(best_tau[:, 0, 0, 0, 0], best_t1[0, 0, :, 0, 0])
    errors = all_stability[:, 0, :, 0, 0]
    figure = plt.figure(figsize=(10, 6))
    ax = figure.add_subplot(111, projection='3d')
    surf = ax.plot_surface(tau_grid, param_gird, errors, cmap='viridis')
    ax.set_xlabel('Tau')
    ax.set_ylabel('T1')
    ax.set_zlabel('Error')
    figure.colorbar(surf, ax=ax, label='Error')
    plt.title('Зависимость ошибки от параметров tau и t1')
    plt.show()
    # Построение поверхности tau, t2
    tau_grid, param_gird = np.meshgrid(best_tau[:, 0, 0, 0, 0], best_t2[0, 0, 0, :, 0])
    errors = all_stability[:, 0, 0, :, 0]
    figure = plt.figure(figsize=(10, 6))
    ax = figure.add_subplot(111, projection='3d')
    surf = ax.plot_surface(tau_grid, param_gird, errors, cmap='viridis')
    ax.set_xlabel('Tau')
    ax.set_ylabel('T2')
    ax.set_zlabel('Error')
    figure.colorbar(surf, ax=ax, label='Error')
    plt.title('Зависимость ошибки от параметров tau и t2')
    plt.show()
    # Построение поверхности tau, d
    tau_grid, param_gird = np.meshgrid(best_tau[:, 0, 0, 0, 0], best_d[0, 0, 0, 0, :])
    errors = all_stability[:, 0, 0, 0, :]
    figure = plt.figure(figsize=(10, 6))
    ax = figure.add_subplot(111, projection='3d')
    surf = ax.plot_surface(tau_grid, param_gird, errors, cmap='viridis')
    ax.set_xlabel('Tau')
    ax.set_ylabel('D')
    ax.set_zlabel('Error')
    figure.colorbar(surf, ax=ax, label='Error')
    plt.title('Зависимость ошибки от параметров tau и d')
    plt.show()


# Начальные параметры
t = 0.00
delta_t = 0.01
t_stop = 10
# Количество итераций типо
n = 3
# Определение диапазонов для перебора параметров
tau_range = np.linspace(0.001, 0.01, n)
k_range = np.linspace(1, 5, n)
t1_range = np.linspace(1, 5, n)
t2_range = np.linspace(1, 5, n)
d_range = np.linspace(0.1, 1, n)

# Подбор лучших параметров
best_param, best_tau, best_k, best_t1, best_t2, best_d = param_sweep(tau_range, k_range, t, delta_t, t_stop, t1_range,
                                                                     t2_range, d_range)
print(f"Лучшие параметры: tau = {best_tau[0]}, k = {best_k[0]}, T1 = {best_t1[0]}, T2 = {best_t2[0]}, D = {best_d[0]}")

best_tau = np.array(best_tau)
best_k = np.array(best_k)
best_t1 = np.array(best_t1)
best_t2 = np.array(best_t2)
best_d = np.array(best_d)

new_tau = best_tau.reshape(n, n, n, n, n)
new_k = best_k.reshape(n, n, n, n, n)
new_t1 = best_t1.reshape(n, n, n, n, n)
new_t2 = best_t2.reshape(n, n, n, n, n)
new_d = best_d.reshape(n, n, n, n, n)

# Симуляция с лучшими параметрами
all_time, all_target_states, all_states, all_stability = simulation(t, delta_t, t_stop, best_tau[0], best_k[0], best_t1[0], best_t2[0], best_d[0])
new_stability = np.array(all_stability[0:243])
new_new_stability = new_stability.reshape(n, n, n, n, n)

plot_results(new_tau, new_k, new_t1, new_t2, new_d, new_new_stability)
