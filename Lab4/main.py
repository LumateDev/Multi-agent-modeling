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


def get_current_state(environment_T1, environment_T2, environment_D, previous_state, previous_state_2, delta_t, current_control):
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

        current_state_minus_tau = state_through_interpolate(all_time, all_states, t - tau)
        current_control = calculate_agent_activity(k, current_target_state, current_state_minus_tau)
        current_state = get_current_state(t1, environment_T2, environment_D, all_states[-1], all_states[-2], delta_t, current_control)
        all_states.append(current_state)

        current_stability = is_converged(current_target_state, current_state)
        all_stability.append(current_stability)

        # Принты для отслеживания состояния
        #print(f"t: {t:.2f}, Target State: {current_target_state}, Current State: {current_state:.4f}, Stability: {current_stability}")

        t += delta_t

    return all_time, all_target_states, all_states, all_stability


def param_sweep(tau_range, k_range, t, delta_t, t_stop, environment_T1, environment_T2, environment_D, t1_range):
    best_params = None
    best_error = float('inf')

    for tau in tau_range:
        for k in k_range:
            for t1 in t1_range:

                all_time, all_target_states, all_states, all_stability = simulation(t, delta_t, t_stop, tau, k, t1, environment_T2, environment_D)
                final_error = np.mean(all_stability)

                # Принт для отслеживания ошибок
                # print(f"Testing tau: {tau:.4f}, k: {k:.4f}, Final Error: {final_error:.4f}")

                if final_error < best_error:
                    best_error = final_error
                    best_params = (tau, k, t1)

    return best_params


# Начальные параметры
t = 0.00
delta_t = 0.01
t_stop = 10
t1 = 1.54
environment_T2 = 2.2
environment_D = 0.9

# Определение диапазонов для перебора параметров
tau_range = np.linspace(0.001, 0.01, 10)
k_range = np.linspace(1, 5, 10)
t1_range = np.linspace(1, 5, 10)

# Подбор лучших параметров
best_tau, best_k, best_t1 = param_sweep(tau_range, k_range, t, delta_t, t_stop, t1, environment_T2, environment_D, t1_range)
print(f"Лучшие параметры: tau = {best_tau}, k = {best_k}, T1 = {best_t1}")

# Симуляция с лучшими параметрами
all_time, all_target_states, all_states, all_stability = simulation(t, delta_t, t_stop, best_tau, best_k, t1, environment_T2, environment_D)

# Построение графика
plt.figure(figsize=(10, 6))
plt.plot(all_time, all_stability, label="Отклонение целевого от полученного", color="red")
plt.plot(all_time, all_states[1:], label="Состояния среды", color="green")
plt.plot(all_time, all_target_states, label="Целевые состояния среды", color="blue")
plt.xlabel("Время")
plt.ylabel("Состояния среды")
plt.title(f"Сравнение результатов (tau = {best_tau}; k = {best_k}; T1 = {best_t1}, T2 = {environment_T2}; D = {environment_D})")
plt.legend()
plt.grid(True)
plt.show()
