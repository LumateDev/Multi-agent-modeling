from matplotlib import pyplot as plt
from collections import defaultdict
import numpy as np

class Graphics:
    def __init__(self, levels, balances, survival_data, max_level):
        """
        Инициализация графического модуля.

        :param levels: Список уровней колоний
        :param balances: Список балансов колоний
        :param survival_data: Список выживших колоний по циклам
        :param max_level: Максимальный уровень колоний
        """

        self.levels = levels
        self.balances = balances
        self.survival_data = survival_data
        self.max_level = max_level
        print(f"Создан Graphics  levels = {levels}, balances = {balances}, survival_data = {survival_data}, max_level = {max_level}")

    def plot_level_distribution(self):
        """Гистограмма распределения уровней колоний."""
        plt.hist(self.levels, bins=range(1, self.max_level + 2), alpha=0.7, color="blue")
        plt.title("Распределение уровней колоний")
        plt.xlabel("Уровень")
        plt.ylabel("Количество")
        plt.show()

    def plot_balance_distribution(self):
        """Гистограмма распределения балансов колоний."""
        plt.hist(self.balances, bins=20, alpha=0.7, color="orange")
        plt.title("Распределение балансов колоний")
        plt.xlabel("Баланс")
        plt.ylabel("Количество")
        plt.show()

    def plot_survival_curve(self):
        """График выживаемости колоний по циклам."""
        plt.plot(self.survival_data, label="Выживаемость", color="green")
        plt.title("График выживаемости колоний")
        plt.xlabel("Цикл")
        plt.ylabel("Количество выживших")
        plt.legend()
        plt.show()

    def plot_average_survival_by_level(self):
        """График средней выживаемости по уровням."""
        survival_by_level = defaultdict(list)

        for level, survival in zip(self.levels, self.survival_data):
            survival_by_level[level].append(survival)

        avg_survival = {level: np.mean(values) for level, values in survival_by_level.items()}

        plt.bar(avg_survival.keys(), avg_survival.values(), alpha=0.7, color="purple")
        plt.title("Средняя выживаемость по уровням")
        plt.xlabel("Уровень")
        plt.ylabel("Средняя выживаемость")
        plt.show()

    def plot_max_level_progression(self, level_progression):
        """График прогресса максимального уровня по циклам."""
        plt.plot(level_progression, label="Максимальный уровень", color="red")
        plt.title("Прогресс максимального уровня")
        plt.xlabel("Цикл")
        plt.ylabel("Максимальный уровень")
        plt.legend()
        plt.show()

    def plot_level_growth_distribution(self, levels_growth):
        """График распределения прироста уровня."""
        plt.hist(levels_growth, bins=20, alpha=0.7, color="cyan")
        plt.title("Распределение прироста уровня")
        plt.xlabel("Прирост уровня")
        plt.ylabel("Количество")
        plt.show()

    def plot_balance_change(self, balances_by_cycle):
        """График изменения балансов колоний по циклам."""
        for i, balances in enumerate(balances_by_cycle):
            plt.plot(balances, label=f"Цикл {i+1}")

        plt.title("Изменение балансов колоний")
        plt.xlabel("Цикл")
        plt.ylabel("Баланс")
        plt.legend()
        plt.show()

    def plot_victory_defeat_distribution(self, victory_levels, defeat_levels):
        """График распределения побед и выбываний."""
        plt.hist(victory_levels, bins=range(1, self.max_level + 2), alpha=0.7, label="Победы", color="green")
        plt.hist(defeat_levels, bins=range(1, self.max_level + 2), alpha=0.7, label="Выбывания", color="red")
        plt.title("Распределение побед и выбываний")
        plt.xlabel("Уровень")
        plt.ylabel("Количество")
        plt.legend()
        plt.show()

    def plot_survival_and_levels(self, level_progression):
        """Сводный график выживаемости и роста максимального уровня."""
        plt.plot(self.survival_data, label="Выживаемость", color="blue")
        plt.plot(level_progression, label="Максимальный уровень", color="green")
        plt.title("Выживаемость и максимальный уровень")
        plt.xlabel("Цикл")
        plt.ylabel("Значения")
        plt.legend()
        plt.show()
