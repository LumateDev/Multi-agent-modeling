class Module:
    def __init__(self, id, load):
        self.id = id
        self.load = load  # Нагрузка
        self.state = "inactive"  # Состояние модуля (inactive/active/completed)