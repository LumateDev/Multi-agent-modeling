from matplotlib import pyplot as plt
from const import MAX_LEVEL

class Graphics:
    def __init__(self, levels, balances, survival_data):
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


