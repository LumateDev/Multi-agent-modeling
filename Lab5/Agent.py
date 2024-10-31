class Agent:
    def __init__(self, id):
        self.id = id
        self.current_module = None  # Текущий обрабатываемый модуль
        self.active = True  # Агент активен по умолчанию

    def assign_module(self, module):
        self.current_module = module
        module.state = "active"
        print(f"Агент {self.id} назначен на модуль {module.id} с нагрузкой {module.load:.2f}")

    def complete_module(self):
        if self.current_module:
            completed_module = self.current_module
            self.current_module.state = "completed"
            self.current_module = None
            return completed_module
        return None

    def fail(self):
        self.active = False
        print(f"Агент {self.id} выбывает из выполнения из-за поломки.")