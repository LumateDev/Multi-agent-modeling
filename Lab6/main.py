import random
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import PillowWriter


class State:
    def __init__(self, agent):
        self.agent = agent

    def update(self):
        pass


class HealthyState(State):
    def __init__(self, agent):
        super().__init__(agent)
        self.agent.speed = self.agent.base_speed

    def update(self):
        # Если агент видит зомби, увеличиваем скорость
        for other in self.agent.simulation.agents:
            if isinstance(other.state, ZombieState) and other.state.distance_to(
                    self.agent) < self.agent.simulation.infection_radius:
                self.agent.speed = self.agent.base_speed * 1.25
                break
        else:
            self.agent.speed = self.agent.base_speed  # Если нет зомби, возвращаем обычную скорость


class InfectedState(State):
    def __init__(self, agent, incubation_period):
        super().__init__(agent)
        self.incubation_period = incubation_period
        self.agent.speed = self.agent.base_speed * 0.95  # скорость снижена

    def update(self):
        self.incubation_period -= 1
        if self.incubation_period <= 0:
            self.agent.state = ZombieState(self.agent)


class ZombieState(State):
    def __init__(self, agent, view_radius=15, view_angle=90):
        super().__init__(agent)
        self.agent.speed = self.agent.base_speed * 0.9  # Зомби движется медленнее
        self.view_radius = view_radius  # Радиус видимости зомби
        self.view_angle = math.radians(view_angle)  # Угол обзора зомби в радианах

    def update(self):
        # Шанс выздороветь с вероятностью 1% на каждой итерации Тут внесена попробовка вероятности чтобы зомби могли победить, при вероятности 1 процент это не происходит
        if random.random() < 0.001:
            self.agent.state = RecoveredState(self.agent)
            return  # Прерываем выполнение, если зомби выздоровел
        # Найти здорового агента в секторе видимости
        target = self.find_visible_healthy_agent()

        if target:
            # Преследование видимого здорового агента
            self.move_toward(target)
            # Проверка на заражение, если агент находится в радиусе действия
            if self.distance_to(target) < self.agent.simulation.infection_radius:
                incubation_period = random.randint(
                    self.agent.simulation.t_inc_min, self.agent.simulation.t_inc_max
                )
                target.state = InfectedState(target, incubation_period)
        else:
            # Случайное блуждание
            self.agent.move_randomly()

    def find_visible_healthy_agent(self):
        closest_agent = None
        min_distance = float("inf")

        for other in self.agent.simulation.agents:
            if isinstance(other.state, HealthyState):
                distance = self.distance_to(other)
                if distance < self.view_radius and self.in_view_angle(other):
                    if distance < min_distance:
                        min_distance = distance
                        closest_agent = other
        return closest_agent

    def in_view_angle(self, other_agent):
        # Проверка, находится ли агент в секторе видимости зомби
        dx, dy = other_agent.x - self.agent.x, other_agent.y - self.agent.y
        angle_to_agent = math.atan2(dy, dx)
        relative_angle = (angle_to_agent - self.agent.direction) % (2 * math.pi)
        # Проверяем, находится ли угол в пределах половины угла обзора зомби
        return abs(relative_angle) < self.view_angle / 2

    def move_toward(self, target_agent):
        dx = target_agent.x - self.agent.x
        dy = target_agent.y - self.agent.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance > 0:
            # Перемещение зомби на большем расстоянии для ускорения преследования
            self.agent.x += (dx / distance) * self.agent.speed
            self.agent.y += (dy / distance) * self.agent.speed
            # Поворот зомби в направлении агента для более точного следования
            self.agent.direction = math.atan2(dy, dx)

    def distance_to(self, other_agent):
        return math.sqrt((self.agent.x - other_agent.x) ** 2 + (self.agent.y - other_agent.y) ** 2)


class RecoveredState(State):
    def __init__(self, agent):
        super().__init__(agent)
        self.agent.speed = self.agent.base_speed

    def update(self):
        # Выздоровевшие агенты должны двигаться случайным образом
        self.agent.move_randomly()

        # Проверка на заражение, если зомби в радиусе действия
        for other in self.agent.simulation.agents:
            if isinstance(other.state, ZombieState) and other.state.distance_to(
                    self.agent) < self.agent.simulation.infection_radius:
                if random.random() < 0.64:  # Вероятность заражения
                    self.agent.state = ZombieState(self.agent)
                    break


class Agent:
    def __init__(self, x, y, state_class, base_speed, simulation):
        self.x = x
        self.y = y
        self.base_speed = base_speed
        self.speed = self.base_speed
        self.simulation = simulation
        self.direction = random.uniform(0, 2 * math.pi)  # направление движения
        self.state = state_class(self)

    def update(self):
        self.state.update()
        self.move()

    def move(self):
        if isinstance(self.state, (HealthyState, InfectedState)):
            self.move_randomly()

    def move_randomly(self):
        self.direction += random.uniform(-0.1, 0.1)
        dx = math.cos(self.direction) * self.speed
        dy = math.sin(self.direction) * self.speed
        self.x += dx
        self.y += dy
        self.check_boundaries()

    def check_boundaries(self):
        if self.x < 0 or self.x > 100:
            self.direction = math.pi - self.direction
        if self.y < 0 or self.y > 100:
            self.direction = -self.direction
        self.x = max(0, min(100, self.x))
        self.y = max(0, min(100, self.y))


class Simulation:
    def __init__(self, n, m, t_init, t_inc_min, t_inc_max, T, infection_radius=1.5):
        self.n = n
        self.m = m
        self.t_init = t_init
        self.t_inc_min = t_inc_min
        self.t_inc_max = t_inc_max
        self.T = T
        self.infection_radius = infection_radius
        self.agents = []
        self.time = 0
        self.init_agents()

    def init_agents(self):
        for _ in range(self.n):
            x, y = random.uniform(0, 100), random.uniform(0, 100)
            agent = Agent(x, y, HealthyState, base_speed=1.0, simulation=self)
            self.agents.append(agent)

    def infect_initial_agents(self):
        infected_agents = random.sample(self.agents, self.m)
        for agent in infected_agents:
            incubation_period = random.randint(self.t_inc_min, self.t_inc_max)
            agent.state = InfectedState(agent, incubation_period)

    def run_step(self):
        if self.time == self.t_init:
            self.infect_initial_agents()

        for agent in self.agents:
            agent.update()

        self.time += 1

    def count_states(self):
        healthy_count = sum(isinstance(agent.state, HealthyState) for agent in self.agents)
        infected_count = sum(isinstance(agent.state, InfectedState) for agent in self.agents)
        zombie_count = sum(isinstance(agent.state, ZombieState) for agent in self.agents)
        recovered_count = sum(isinstance(agent.state, RecoveredState) for agent in self.agents)
        return healthy_count, infected_count, zombie_count, recovered_count

    def is_finished(self):
        healthy_count, infected_count, zombie_count, recovered_count = self.count_states()

        # Игра заканчивается, если время превысило T
        if self.time >= self.T:
            return True

        # Игра заканчивается, если все агенты стали зомби или все выздоровели
        if zombie_count == self.n or recovered_count == self.n:
            return True

        # Игра продолжается, если есть хотя бы один инфицированный агент
        if infected_count > 0:
            return False

        # Если есть ещё инкубационные агенты, игра продолжается
        for agent in self.agents:
            if isinstance(agent.state, InfectedState) and agent.state.incubation_period > 0:
                return False

        # Если все агенты стали зомби или выздоровели, игра завершается
        if zombie_count == self.n or recovered_count == self.n:
            return True

        # Игра продолжается, если есть зомби или инфицированные агенты
        return False


def animate(i, sim, scat, text):
    sim.run_step()
    x_data = [agent.x for agent in sim.agents]
    y_data = [agent.y for agent in sim.agents]
    colors = [
        "blue" if isinstance(agent.state, HealthyState) else
        "orange" if isinstance(agent.state, InfectedState) else
        "red" if isinstance(agent.state, ZombieState) else
        "green"
        for agent in sim.agents
    ]
    scat.set_offsets(list(zip(x_data, y_data)))
    scat.set_color(colors)

    healthy, infected, zombies, recovered = sim.count_states()
    text.set_position((0.05, 0.95))  # Размещение текста в верхнем левом углу
    text.set_text(
        f"Time: {sim.time}\nHealthy: {healthy}\nInfected: {infected}\nZombies: {zombies}\nRecovered: {recovered}"
    )

    if sim.is_finished():
        ani.event_source.stop()  # Остановка анимации


def run_experiments():
    # Заданные значения для n (количество агентов) и m (количество зараженных агентов)
    n_values = [50, 50, 100, 100]
    m_values = [5, 20, 10, 40]
    results = []

    for i in range(len(n_values)):
        n = n_values[i]
        m = m_values[i]

        total_time = 0

        # Проведем 1000 экспериментов для каждой конфигурации
        print(f"\nЗапуск экспериментов для n={n}, m={m}... (1000 экспериментов)")

        for exp_num in range(1, 1001):
            sim = Simulation(n=n, m=m, t_init=10, t_inc_min=5, t_inc_max=10, T=1000)

            while not sim.is_finished():
                sim.run_step()
            # print(f"experiment {exp_num} time {sim.time}")
            total_time += sim.time  # Суммируем время, за которое вся популяция превращается в зомби

            if exp_num % 100 == 0:  # Каждые 100 экспериментов выводим информацию
                print(f"    Пройдено {exp_num} экспериментов...")
                print(f"    Среднее время: {total_time / exp_num:.2f} единиц времени")

        avg_time = total_time / 1000  # Среднее время для этой конфигурации
        results.append((n, m, avg_time))  # Добавляем результат

        print(f"Эксперименты завершены для n={n}, m={m}. Среднее время: {avg_time:.2f} единиц времени\n")

    # Выводим таблицу результатов
    print("\nТаблица результатов:")
    print("n\tm\tСреднее время (Единицы времени)")
    for n, m, avg_time in results:
        print(f"{n}\t{m}\t{avg_time:.2f}")


def run_with_plot(sim):
    fig, ax = plt.subplots()
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    scat = ax.scatter([], [], s=10)
    text = ax.text(1, 1, "", va="top", ha="left", fontsize=10, color="black", transform=ax.transAxes)

    global ani
    ani = animation.FuncAnimation(
        fig, animate, fargs=(sim, scat, text), interval=50, cache_frame_data=False
    )
    plt.show()


def save_video(sim, filename='simulation.gif', fps=20):
    fig, ax = plt.subplots()
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    scat = ax.scatter([], [], s=10)
    text = ax.text(1, 1, "", va="top", ha="left", fontsize=10, color="black", transform=ax.transAxes)

    global ani

    ani = animation.FuncAnimation(
        fig, animate, fargs=(sim, scat, text), frames=sim.T, interval=50, cache_frame_data=False
    )

    # Сохранение анимации в GIF, используя PillowWriter
    writer = PillowWriter(fps=fps)
    ani.save(filename, writer=writer)


def main():
    sim = Simulation(n=100, m=5, t_init=10, t_inc_min=5, t_inc_max=10, T=1000)
    run_with_plot(sim)
    save_video(sim, 'simulation.gif')

    # run_experiments()


if __name__ == "__main__":
    main()
