class Agent:
    def __init__(self, agent_id):
        self.agent_id = agent_id
        self.queue = []  # Очередь клиентов для обслуживания
        self.total_clients_served = 0  # Обслуженные клиенты
        self.total_service_time = 0  # Общее время на обслуживание всех клиентов
        self.remaining_service_time = 0  # Время на завершение текущего обслуживания

    def add_client_to_queue(self, client):
        self.queue.append(client)
        # Если агент не занят, начинаем обслуживание нового клиента
        if self.remaining_service_time == 0 and self.queue:
            self.start_service()

    def start_service(self):
        if self.queue:
            client = self.queue.pop(0)
            self.remaining_service_time = client.complexity
            self.total_clients_served += 1
            self.total_service_time += client.complexity

    def update(self):
        """Обновление времени обслуживания и переход к следующему клиенту."""
        if self.remaining_service_time > 0:
            self.remaining_service_time -= 1
        if self.remaining_service_time == 0 and self.queue:
            self.start_service()

    def get_agent_load(self):
        queue_load = sum(client.complexity for client in self.queue)
        return self.remaining_service_time + queue_load

    def __str__(self):
        return (f"Агент {self.agent_id}: Обслуженно клиентов: {self.total_clients_served}, "
                f"Потрачено времени на обслуживание: {self.total_service_time}")