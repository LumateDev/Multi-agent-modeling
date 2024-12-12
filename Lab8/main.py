import random
import matplotlib.pyplot as plt
import pandas as pd

# Константы и начальные настройки
MAX_LEVEL = 10
INITIAL_BALANCE = 100  # Уменьшен для восприятия
EXPERIENCE_THRESHOLD = 200  # Уменьшен для более быстрого роста уровней
COLONY_COUNT = 10
SIMULATION_TIME = 1000
ITERATIONS_PER_CYCLE = 10
AUCTION_INTERVAL = 5
EVENT_INTERVAL = 7
LOG_FILE = "simulation_log.txt"


class Colony:
    def __init__(self, name, balance, income, expenses):
        self.name = name
        self.level = 1
        self.balance = balance
        self.income = income
        self.expenses = expenses
        self.experience = 0
        self.artifact = None
        self.alive = True
        self.is_winner = False  # Новый флаг для победителей
        self.rounds_played = 0  # Количество раундов участия
        self.level_up_iteration = None  # Итерация достижения уровня 10
        self.termination_iteration = None  # Итерация завершения игры

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
                # Победитель исключается из дальнейшего участия
                self.alive = False

    def update_balance(self, log):
        if not self.alive:  # Если колония уже выбыла или победила, ничего не делаем
            return

        previous_balance = self.balance
        self.balance += self.income - self.expenses
        self.experience += max(0, self.balance - previous_balance) // 100  # Медленное накопление опыта

        if self.balance < 0:  # Баланс отрицательный
            if self.level == MAX_LEVEL and self.is_winner:  # Если это победитель — баланс игнорируется
                log.append(f"{self.name}: Победитель! Баланс стал отрицательным, но статус не изменён.")
            else:
                self.alive = False
                self.is_winner = False  # Убедимся, что статус победителя не будет установлен
                self.termination_iteration = self.rounds_played  # Фиксируем итерацию выбытия
                log.append(f"{self.name}: Баланс отрицателен, колония выбывает!")
                return

    def apply_artifact(self, log):
        if self.artifact:
            self.artifact.apply(self, log)
            if self.artifact.duration == 0:
                log.append(f"{self.name}: Артефакт перестал действовать.")
                self.artifact = None

    def __str__(self):
        status = "Победитель" if self.is_winner else ("Выбыла" if not self.alive else "Активна")
        return f"{self.name} (Уровень: {self.level}, Баланс: {self.balance:.2f}, Доход: {self.income:.2f}, Расходы: {self.expenses:.2f}, Статус: {status})"


class Artifact:
    def __init__(self, effect, duration, name):
        self.effect = effect
        self.duration = duration
        self.name = name

    def apply(self, colony, log):
        if self.duration > 0:
            self.effect(colony, log)
            self.duration -= 1
            log.append(f"Артефакт '{self.name}' применён к {colony.name}. Осталось итераций: {self.duration}.")


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
    colony.alive = False
    log.append(f"{colony.name}: Артефакт установил максимальный уровень! Колония завершила игру.")


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
def run_cycle(colonies, cycle_number, log):
    log.append(f"\nЦикл {cycle_number}: Начало.")
    for colony in colonies:
        colony.rounds_played += 1
        colony.update_balance(log)
        colony.check_level_up(log, cycle_number)
        colony.apply_artifact(log)

    if cycle_number % EVENT_INTERVAL == 0:
        event = random.choice([dust_storm, renaissance])
        log.append("\nСобытие среды:")
        for colony in colonies:
            if colony.alive:
                event(colony, log)

    if cycle_number % AUCTION_INTERVAL == 0:
        run_auction(colonies, log)


def run_auction(colonies, log):
    log.append("\nАукцион начинается.")
    active_colonies = [c for c in colonies if c.alive and not c.artifact]
    if not active_colonies:
        log.append("Нет доступных колоний для участия в аукционе.")
        return

    artifact_pool = [
        Artifact(lambda c, l: increase_income(c, l, 10), 3, "Увеличение дохода на 10%"),
        Artifact(lambda c, l: decrease_expenses(c, l, 15), 3, "Снижение расходов на 15%"),
        Artifact(lambda c, l: boost_balance(c, l, 20), 1, "Увеличение баланса на 20%"),
        Artifact(max_level_artifact, 1, "Установить максимальный уровень")
    ]

    for artifact in artifact_pool:
        bidders = [c for c in active_colonies if c.balance > 50]
        if not bidders:
            break

        winner = random.choice(bidders)
        winner.artifact = artifact
        active_colonies.remove(winner)  # Исключаем из повторной покупки
        log.append(f"{winner.name} приобрела артефакт: {artifact.name}.")


# Инициализация колоний
colonies = [
    Colony(f"Колония {i + 1}", INITIAL_BALANCE, random.randint(10, 50), random.randint(5, 30))
    for i in range(COLONY_COUNT)
]

# Запуск симуляции
log = []
survival_data = []
for cycle in range(1, SIMULATION_TIME + 1):
    run_cycle(colonies, cycle, log)

    # Проверка завершения симуляции, если все колонии достигли уровня 10 или выбыли
    if all(c.level == MAX_LEVEL or not c.alive for c in colonies):
        break

    # Сбор данных для графика
    survival_data.append(sum(1 for c in colonies if c.alive))

# Сохранение лога в файл
with open(LOG_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(log))

# Построение графиков
levels = [c.level for c in colonies]
balances = [c.balance for c in colonies]

plt.hist(levels, bins=range(1, MAX_LEVEL + 2), alpha=0.7, label="Уровни")
plt.title("Распределение уровней колоний")
plt.xlabel("Уровень")
plt.ylabel("Количество")
plt.show()

plt.hist(balances, bins=20, alpha=0.7, label="Балансы")
plt.title("Распределение балансов колоний")
plt.xlabel("Баланс")
plt.ylabel("Количество")
plt.show()

plt.plot(survival_data, label="Выживание колоний")
plt.title("График выживаемости колоний")
plt.xlabel("Цикл")
plt.ylabel("Количество выживших")
plt.legend()
plt.show()

# Сбор итоговой таблицы
# Сбор итоговой таблицы
colony_info = [
    {
        "Название": c.name,
        "Уровень": c.level,
        "Баланс": c.balance,
        "Статус": "Победитель" if c.is_winner else ("Выбыла" if not c.alive else "Активна"),
        "Раунды сыграно": c.rounds_played,
        "Итерация достижения максимального уровня": c.level_up_iteration if c.is_winner else "Не достиг",
        "Причина выбытия": "Баланс отрицателен" if not c.alive else "Не выбыла",
        "Итерация завершения": cycle if not c.alive else "Не завершена"
    } for c in colonies
]

pd.set_option('display.max_rows', None)  # Показывать все строки
pd.set_option('display.max_columns', None)  # Показывать все столбцы
df = pd.DataFrame(colony_info)
print(df)
