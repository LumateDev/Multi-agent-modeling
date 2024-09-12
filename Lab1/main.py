from Enviroment import Environment

if __name__ == '__main__':
    num_agents = 3  # Количество агентов
    a = 1  # Начало интервала для появления нового клиента (время)
    b = 5  # Конец интервала для появления нового клиента (время)
    m = 10  # Номер последнего клиента, которого нужно обслужить

    env = Environment(num_agents, a, b)
    env.run_simulation(m)