import matplotlib.pyplot as plt
import numpy as np

# Данные
strategies = [
    'aggressive_strategy', 'enhanced_defensive_strategy', 'random_strategy', 'balanced_trap_strategy'
]

results = {
    'aggressive_strategy': {
        'aggressive_strategy': (39.8, 60.2),
        'enhanced_defensive_strategy': (38.7, 61.3),
        'random_strategy': (40.9, 59.1),
        'balanced_trap_strategy': (41.2, 58.8),
    },
    'enhanced_defensive_strategy': {
        'aggressive_strategy': (44.4, 55.6),
        'enhanced_defensive_strategy': (39.4, 60.6),
        'random_strategy': (42.6, 57.4),
        'balanced_trap_strategy': (42.2, 57.8),
    },
    'random_strategy': {
        'aggressive_strategy': (43.4, 56.6),
        'enhanced_defensive_strategy': (38.4, 61.6),
        'random_strategy': (41.9, 58.1),
        'balanced_trap_strategy': (40.9, 59.1),
    },
    'balanced_trap_strategy': {
        'aggressive_strategy': (38.1, 61.9),
        'enhanced_defensive_strategy': (41.7, 58.3),
        'random_strategy': (38.4, 61.6),
        'balanced_trap_strategy': (39.9, 60.1),
    }
}

# Создание графика
fig, ax = plt.subplots(figsize=(10, 8))

# Список индексов для стратегии
x = np.arange(len(strategies))

# Вычисление ширины баров
width = 0.35

# Позиции для пар
x_positions = x - width / 2

# Построение баров для каждой стратегии
for i, strategy in enumerate(strategies):
    pair1_wins = [results[strategy][other][0] for other in strategies]
    pair2_wins = [results[strategy][other][1] for other in strategies]

    ax.bar(x_positions + width * i, pair1_wins, width, label=f'{strategy} - Pairs 1 Wins')
    ax.bar(x_positions + width * i, pair2_wins, width, bottom=pair1_wins, label=f'{strategy} - Pairs 2 Wins')

# Настройки графика
ax.set_xlabel('Strategy Comparison')
ax.set_ylabel('Win Percentage')
ax.set_title('Comparison of Strategy Pairs Wins')
ax.set_xticks(x)
ax.set_xticklabels(strategies)
ax.legend()

# Отображение
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
