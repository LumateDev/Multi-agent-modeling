from const import EXPERIENCE_THRESHOLD, MAX_LEVEL

class Colony:
    def __init__(self, name, balance, income, expenses):
        self.name = name
        self.level = 1
        self.balance = balance
        self.income = income
        self.expenses = expenses
        self.experience = 0
        self.effects = []  # Новый список для активных эффектов
        self.alive = True
        self.is_winner = False
        self.rounds_played = 0
        self.level_up_iteration = None

    def check_level_up(self, log, cycle_number):
        if not self.alive:  # Если колония уже выбыла, не выполняем дальнейшую логику
            return

        # Проверяем, достигла ли колония уровня 10
        if self.level < MAX_LEVEL and self.experience >= EXPERIENCE_THRESHOLD:
            self.experience = 0
            self.level += 1
            log.append(f"{self.name}: Повышение уровня! Новый уровень: {self.level}.")

        if self.level == MAX_LEVEL:  # Если достигнут максимальный уровень
            self.is_winner = True  # Помечаем как победителя
            self.level_up_iteration = cycle_number  # Фиксируем итерацию достижения 10 уровня
            log.append(f"{self.name}: Достигнут максимальный уровень и назначена как победитель.")
            self.alive = False  # Колония больше не участвует в игре, она победила
            return  # Завершаем функцию, так как колония больше не будет участвовать в цикле

    def update_balance(self, log):
        if not self.alive:  # Если колония уже выбыла или победила, ничего не делаем
            return



        previous_balance = self.balance
        self.balance += self.income - self.expenses
        self.experience += max(0, self.balance - previous_balance) // 90
        self.experience += self.income // 10

        if self.balance < 0:  # Баланс отрицательный
            self.alive = False
            log.append(f"{self.name}: Баланс отрицателен, колония выбывает!")

    def apply_effects(self, log):
        """Применить все активные эффекты к колонии"""
        for effect in self.effects:
            effect.apply(self, log)
            effect.duration -= 1

        # Удаляем эффекты с завершённым сроком действия
        expired_effects = [e for e in self.effects if e.duration <= 0 and e.name != "Максимальный уровень"]
        for effect in expired_effects:
            effect.rollback(self, log)
            log.append(f"{self.name}: Эффект '{effect.name}' истёк.")
            self.effects.remove(effect)

    def __str__(self):
        status = "Победитель" if self.is_winner else ("Выбыла" if not self.alive else "Активна")
        return f"{self.name} (Уровень: {self.level}, Баланс: {self.balance:.2f}, Доход: {self.income:.2f}, Расходы: {self.expenses:.2f}, Статус: {status})"