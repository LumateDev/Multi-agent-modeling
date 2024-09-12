import random
from Agent import Agent
from Client import Client


class Environment:
    def __init__(self, num_agents, a, b):
        self.agents = [Agent(agent_id) for agent_id in range(num_agents)]
        self.client_id_counter = 1  # Уникальный идентификатор клиентов
        self.a = a  # Минимальный интервал времени между появлениями клиентов
        self.b = b  # Максимальный интервал времени между появлениями клиентов

    def generate_random_client(self):
        complexity = random.randint(1, 10)
        client = Client(self.client_id_counter, complexity)
        print(f"Новый клиент {self.client_id_counter} появился со сложностью: {complexity}")
        self.client_id_counter += 1
        return client

    def find_least_loaded_agent(self):
        agent_loads = [f"Агент {agent.agent_id} загружен на {agent.get_agent_load()}" for agent in self.agents]
        print(f"Текущая загрузка агентов: {agent_loads}")
        return min(self.agents, key=lambda agent: agent.get_agent_load())

    def run_simulation(self, m):
        time = 0
        clients_served = 0

        while clients_served < m:
            # Новый клиент появляется через случайный интервал времени
            new_client_interval = random.uniform(self.a, self.b)
            time += new_client_interval

            # Появляется новый клиент
            new_client = self.generate_random_client()

            # Находим агента с минимальной загрузкой
            chosen_agent = self.find_least_loaded_agent()
            print(f"Клиент {new_client.client_id} назначен агенту {chosen_agent.agent_id}")

            # Добавляем клиента в очередь выбранного агента
            chosen_agent.add_client_to_queue(new_client)

            # Обновляем время у всех агентов
            for agent in self.agents:
                agent.update()

            clients_served += 1

        self.generate_report()

    def generate_report(self):
        agents_report = sorted(self.agents, key=lambda agent: (-agent.total_clients_served, agent.total_service_time))
        print("\n--- Итоговый отчет агентов ---")
        for agent in agents_report:
            print(agent)
