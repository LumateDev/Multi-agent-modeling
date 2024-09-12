class Client:
    def __init__(self, client_id, complexity):
        self.client_id = client_id
        self.complexity = complexity  # Сложность обслуживания = время на обслуживание

    def __str__(self):
        return f"Client {self.client_id}, complexity {self.complexity}"