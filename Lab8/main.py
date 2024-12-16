import random
import pandas as pd
from Graphics import Graphics
from const import *
from Effect import Effect
from Colony import Colony
from Artifact import Artifact
from Environment import dust_storm,renaissance

# Функции симуляции
def run_cycle(active_colonies, winners, losers, cycle_number, log):
    log.append(f"\nЦикл {cycle_number}: Начало.")

    for colony in active_colonies[:]:
        if colony.is_winner:  # Если колония победила, пропускаем её обновление
            winners.append(colony)  # Добавляем победителей в список
            active_colonies.remove(colony)  # Убираем победителя из активных колоний
            continue

        colony.rounds_played += 1
        colony.apply_effects(log)
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
    # Артефакт 77:
    Artifact("Увеличение дохода", [Effect('income', 10, 3, "Увеличение дохода на 10%")]),

    # Артефакт 73:
    Artifact("Снижение расходов", [Effect('expenses', 15, 3, "Снижение расходов на 15%")]),

    # Артефакт 53:
    Artifact("Увеличение баланса", [Effect('balance', 20, 3, "Увеличение баланса на 20%")]),

    # Артефакт 3:
    Artifact("Максимальный уровень", [Effect('level', MAX_LEVEL, 1, "Максимальный уровень")]),  # Используем новый эффект для установки максимального уровня

    # Артефакт 4:
    Artifact("Текущий расход - {n}", [
        Effect('expenses', 10, 3, "Текущий расход - 10% от баланса"),
        Effect('balance', 15, 3, "Баланс увеличен на 15% от дохода")
    ]),
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
level_progression = []
levels_growth = []
balances_by_cycle = []
victory_levels = []
defeat_levels = []

previous_total_level = sum(colony.level for colony in colonies)  # Для расчёта роста уровней


for cycle in range(1, SIMULATION_TIME + 1):
    if not active_colonies:  # Если активных колоний больше нет, завершить симуляцию
        break

    run_cycle(active_colonies, winners, losers, cycle, log)

    # Обновление данных для графиков
    # 1. Прогресс уровней (средний уровень)
    avg_level = sum(colony.level for colony in active_colonies) / max(1, len(active_colonies))
    level_progression.append(avg_level)

    # 2. Прирост уровней
    current_total_level = sum(colony.level for colony in active_colonies)
    levels_growth.append(current_total_level - previous_total_level)
    previous_total_level = current_total_level

    # 3. Балансы по циклам
    balances_by_cycle.append([colony.balance for colony in active_colonies])

    # 4. Уровни победителей
    for winner in winners:
        if winner.level not in victory_levels:
            victory_levels.append(winner.level)

    # 5. Уровни выбывших
    for loser in losers:
        if loser.level not in defeat_levels:
            defeat_levels.append(loser.level)

    # Сохраняем количество выживших для графика выживаемости
    survival_data.append(len(active_colonies))

# Сохранение лога в файл
with open(LOG_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(log))

# Построение графиков

levels = [c.level for c in colonies]
balances = [c.balance for c in colonies]

# graphics = Graphics(levels=levels, balances=balances, survival_data=survival_data, max_level=MAX_LEVEL)
# graphics.plot_level_distribution()
# graphics.plot_balance_distribution()
# graphics.plot_survival_curve()
#
#
# # Дополнительные графики с динамически посчитанными данными
# graphics.plot_average_survival_by_level()
# graphics.plot_max_level_progression(level_progression)
# graphics.plot_level_growth_distribution(levels_growth)
# graphics.plot_balance_change(balances_by_cycle)
# graphics.plot_victory_defeat_distribution(victory_levels, defeat_levels)
# graphics.plot_survival_and_levels(level_progression)


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
