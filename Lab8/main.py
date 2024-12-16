import random
import pandas as pd
from Graphics import Graphics
from const import *

class Effect:
    def __init__(self, effect_type, value, duration, name):
        self.effect_type = effect_type  # Тип эффекта: 'income', 'expenses', 'balance'
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
        if not self.alive:  # Проверяем, что колония жива
            return

        if self.experience >= EXPERIENCE_THRESHOLD:
            self.experience = 0
            if self.level < MAX_LEVEL:
                self.level += 1
                log.append(f"{self.name}: Повышение уровня! Новый уровень: {self.level}.")

            if self.level == MAX_LEVEL:  # Если достигнут максимальный уровень
                self.is_winner = True
                self.level_up_iteration = cycle_number  # Фиксируем итерацию достижения 10 уровня
                log.append(f"{self.name}: Достигнут максимальный уровень и назначена как победитель.")
                self.alive = False

    def update_balance(self, log):
        if not self.alive:  # Если колония уже выбыла или победила, ничего не делаем
            return

        previous_balance = self.balance
        self.balance += self.income - self.expenses
        self.experience += max(0, self.balance - previous_balance) // 100
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
        expired_effects = [e for e in self.effects if e.duration <= 0]
        for effect in expired_effects:
            effect.rollback(self, log)
            log.append(f"{self.name}: Эффект '{effect.name}' истёк.")
            self.effects.remove(effect)

    def __str__(self):
        status = "Победитель" if self.is_winner else ("Выбыла" if not self.alive else "Активна")
        return f"{self.name} (Уровень: {self.level}, Баланс: {self.balance:.2f}, Доход: {self.income:.2f}, Расходы: {self.expenses:.2f}, Статус: {status})"


class Artifact:
    def __init__(self, name, effects):
        self.name = name
        self.effects = effects

    def apply_artifact(self, colony, log):
        """Применение артефакта добавляет его эффекты в список"""
        for effect in self.effects:
            colony.effects.append(effect)
        log.append(f"{colony.name}: Артефакт '{self.name}' применён.")



# Примеры эффектов артефактов
def increase_income(colony, log, percent=10):
    colony.income += colony.income * (percent / 100)
    log.append(f"{colony.name}: Доход увеличен на {percent}%.")


def decrease_expenses(colony, log, percent=10):
    colony.expenses -= colony.expenses * (percent / 100)
    colony.expenses = max(1, colony.expenses)  # Минимальный расход
    log.append(f"{colony.name}: Расходы уменьшены на {percent}%.")


def boost_balance(colony, log, percent=20):
    colony.balance += colony.balance * (percent / 100)
    log.append(f"{colony.name}: Баланс увеличен на {percent}%.")


def max_level_artifact(colony, log):
    colony.level = MAX_LEVEL
    colony.is_winner = True  # Устанавливаем статус победителя
    colony.level_up_iteration = colony.rounds_played  # Фиксируем раунды до достижения 10 уровня
    colony.alive = False  # Колония завершает участие
    log.append(f"{colony.name}: Артефакт установил максимальный уровень! Колония завершила игру и стала победителем.")



# Примеры событий среды
def dust_storm(colony, log, income_reduction=20, expense_increase=10):
    colony.income -= colony.income * (income_reduction / 100)
    colony.expenses += colony.expenses * (expense_increase / 100)
    log.append(
        f"{colony.name}: Пыльная буря! Доход уменьшен на {income_reduction}%, расходы увеличены на {expense_increase}%.")


def renaissance(colony, log, income_increase=20, expense_reduction=10):
    colony.income += colony.income * (income_increase / 100)
    colony.expenses -= colony.expenses * (expense_reduction / 100)
    colony.expenses = max(1, colony.expenses)
    log.append(
        f"{colony.name}: Ренессанс! Доход увеличен на {income_increase}%, расходы уменьшены на {expense_reduction}%.")


# Функции симуляции
def run_cycle(active_colonies, winners, losers, cycle_number, log):
    log.append(f"\nЦикл {cycle_number}: Начало.")

    for colony in active_colonies[:]:
        colony.rounds_played += 1
        colony.apply_effects(log)  # Применяем все активные эффекты
        colony.update_balance(log)
        colony.check_level_up(log, cycle_number)

        if not colony.alive:
            if colony.is_winner:
                winners.append(colony)
            else:
                losers.append(colony)
            active_colonies.remove(colony)

    if cycle_number % EVENT_INTERVAL == 0:
        event = random.choice([dust_storm, renaissance])
        log.append("\nСобытие среды:")
        for colony in active_colonies:
            event(colony, log)

    if cycle_number % AUCTION_INTERVAL == 0:
        run_auction(active_colonies, log)

artifact_pool = [
    Artifact("Увеличение дохода", [Effect('income', 10, 3, "Увеличение дохода на 10%")]),
    Artifact("Снижение расходов", [Effect('expenses', 15, 3, "Снижение расходов на 15%")]),
    Artifact("Увеличение баланса", [Effect('balance', 20, 3, "Увеличение баланса на 20%")]),
    Artifact("Максимальный уровень", [Effect('balance', 0, 1, "Максимальный уровень")]),
]


def run_auction(active_colonies, log):
    log.append("\nАукцион начинается.")
    active_bidders = [c for c in active_colonies if c.balance > 50]
    if not active_bidders:
        log.append("Нет доступных колоний для участия в аукционе.")
        return

    for artifact in artifact_pool:
        if not active_bidders:
            break
        winner = random.choice(active_bidders)
        log.append(f"{winner.name} приобрела артефакт: {artifact.name}.")
        artifact.apply_artifact(winner, log)  # Используем метод Artifact для применения
        active_bidders.remove(winner)





# Инициализация колоний
colonies = [
    Colony(f"Колония {i + 1}", INITIAL_BALANCE, random.randint(10, 50), random.randint(5, 30))
    for i in range(COLONY_COUNT)
]

# Запуск симуляции
log = []
active_colonies = colonies[:]
winners = []
losers = []
survival_data = []

for cycle in range(1, SIMULATION_TIME + 1):
    if not active_colonies:  # Если активных колоний больше нет, завершить симуляцию
        break

    run_cycle(active_colonies, winners, losers, cycle, log)
    survival_data.append(len(active_colonies))

# Сохранение лога в файл
with open(LOG_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(log))

# Построение графиков

levels = [c.level for c in colonies]
balances = [c.balance for c in colonies]
graphics = Graphics(levels,balances,survival_data)




# Сбор итоговой таблицы
colony_info = [
    {
        "Название": c.name,
        "Уровень": c.level,
        "Баланс": c.balance,
        "Статус": "Победитель" if c in winners else ("Выбыла" if c in losers else "Активна"),
        "Раунды сыграно": c.rounds_played,
        "Итерация достижения максимального уровня": c.level_up_iteration if c.is_winner else "Не достиг",
        "Причина выбытия": "Баланс отрицателен" if c in losers else "Не выбыла",
    } for c in colonies
]


pd.set_option('display.max_rows', None)  # Показывать все строки
pd.set_option('display.max_columns', None)  # Показывать все столбцы
df = pd.DataFrame(colony_info)
print(df)
