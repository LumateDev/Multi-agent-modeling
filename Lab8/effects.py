from const import MAX_LEVEL
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