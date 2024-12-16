from const import MAX_LEVEL

class Effect:
    def __init__(self, effect_type, value, duration, name):
        self.effect_type = effect_type  # Тип эффекта: 'income', 'expenses', 'balance', 'level'
        self.value = value  # Значение изменения: абсолютное или процентное
        self.duration = duration  # Количество итераций
        self.name = name  # Имя эффекта для логирования

    def apply(self, colony, log):
        """Применяет эффект к целевой колонии"""
        if self.effect_type == 'income':
            colony.income += colony.income * (self.value / 100)
            log.append(f"{colony.name}: Доход увеличен на {self.value}%.")
        elif self.effect_type == 'expenses':
            colony.expenses -= colony.expenses * (self.value / 100)
            colony.expenses = max(1, colony.expenses)  # Минимальные расходы — 1
            log.append(f"{colony.name}: Расходы уменьшены на {self.value}%.")
        elif self.effect_type == 'balance':
            colony.balance += colony.balance * (self.value / 100)
            log.append(f"{colony.name}: Баланс увеличен на {self.value}%.")
        elif self.effect_type == 'level':
            # Применение артефакта "Максимальный уровень"
            colony.level = MAX_LEVEL  # Устанавливаем максимальный уровень
            colony.status = "Максимальный уровень"  # Обновляем статус
            log.append(f"{colony.name}: Уровень установлен на {colony.level}. Статус: {colony.status}.")

    def rollback(self, colony, log):
        """Снимает эффект с колонии"""
        if self.effect_type == 'income':
            colony.income -= colony.income * (self.value / 100)
            log.append(f"{colony.name}: Эффект на доход ({self.value}%) снят.")
        elif self.effect_type == 'expenses':
            colony.expenses += colony.expenses * (self.value / 100)
            log.append(f"{colony.name}: Эффект на расходы ({self.value}%) снят.")
        elif self.effect_type == 'balance':
            colony.balance -= colony.balance * (self.value / 100)
            log.append(f"{colony.name}: Эффект на баланс ({self.value}%) снят.")
