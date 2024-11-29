from Agent import *
from GameEnvironment import *


# Стратегии
def aggressive_strategy(agent, env, role, partner_hand):
    if role == "attacker":
        return max(agent.hand, key=lambda x: x.rank)  # Атакует самой сильной картой
    elif role == "defender":
        attacking_card = env.table[-1]
        valid_moves = [card for card in agent.hand if card.suit == attacking_card.suit and card.rank > attacking_card.rank]
        return max(valid_moves, key=lambda x: x.rank, default=None)  # Отбивает самой сильной картой

def defensive_strategy(agent, env, role, partner_hand):
    if role == "attacker":
        return min(agent.hand, key=lambda x: x.rank)  # Атакует самой слабой картой
    elif role == "defender":
        attacking_card = env.table[-1]
        valid_moves = [card for card in agent.hand if card.suit == attacking_card.suit and card.rank > attacking_card.rank]
        return min(valid_moves, key=lambda x: x.rank, default=None)  # Отбивает самой слабой картой

def random_strategy(agent, env, role, partner_hand):
    return random.choice(agent.hand)  # Выбирает случайную карту

def trap_strategy(agent, env, role, partner_hand):
    if role == "attacker":
        # Если у партнера сильная карта, то атакуем слабой картой для отманки
        if partner_hand and max(partner_hand, key=lambda x: x.rank).rank >= 12:
            return min(agent.hand, key=lambda x: x.rank)  # Атакуем самой слабой картой
        return max(agent.hand, key=lambda x: x.rank)  # Иначе атакуем самой сильной картой
    elif role == "defender":
        # Если на столе карта сильная, отбиваем самой сильной
        attacking_card = env.table[-1]
        valid_moves = [card for card in agent.hand if card.suit == attacking_card.suit and card.rank > attacking_card.rank]
        if valid_moves:
            return max(valid_moves, key=lambda x: x.rank)
        return None  # Не можем отбить


# Обновленная стратегия для более сбалансированной игры

# Стратегия защиты
def enhanced_defensive_strategy(agent, env, role, partner_hand):
    if role == "attacker":
        # Атака на слабые карты (например, минимальная карта)
        return min(agent.hand, key=lambda x: x.rank)
    elif role == "defender":
        attacking_card = env.table[-1]
        valid_moves = [card for card in agent.hand if
                       card.suit == attacking_card.suit and card.rank > attacking_card.rank]

        # Усиление защиты, если у партнера хорошая карта
        if valid_moves:
            return max(valid_moves, key=lambda x: x.rank)

        # Иначе отбиваем самой слабой картой
        return min(agent.hand, key=lambda x: x.rank, default=None)


# Стратегия ловушки, немного более сбалансированная
def balanced_trap_strategy(agent, env, role, partner_hand):
    if role == "attacker":
        # Если у партнера сильная карта, атакуем слабыми
        if partner_hand and max(partner_hand, key=lambda x: x.rank).rank >= 12:
            return min(agent.hand, key=lambda x: x.rank)  # Атакуем самой слабой картой
        return max(agent.hand, key=lambda x: x.rank)  # Иначе атакуем самой сильной картой
    elif role == "defender":
        # Улучшенная защита, проверка всех карт для отбивания
        attacking_card = env.table[-1]
        valid_moves = [card for card in agent.hand if
                       card.suit == attacking_card.suit and card.rank > attacking_card.rank]
        if valid_moves:
            return max(valid_moves, key=lambda x: x.rank)
        return None  # Если не можем отбить


# Логика игры
def play_game(agent1_strategy, agent2_strategy):
    env = GameEnvironment()
    agents = [
        Agent(0, agent1_strategy),  # Пара 1
        Agent(1, agent1_strategy),
        Agent(2, agent2_strategy),  # Пара 2
        Agent(3, agent2_strategy)
    ]
    env.deal()
    scores = [0, 0]  # Победные очки для пары 1 и пары 2
    current_attacker = min(range(4),
                           key=lambda i: min(env.hands[i], key=lambda x: (x.suit != env.trump.suit, x.rank)).rank)
    defending_team = (current_attacker + 2) % 4

    while True:
        if all(not env.hands[i] for i in range(2)):
            return 0  # Победила пара 1
        if all(not env.hands[i] for i in range(2, 4)):
            return 1  # Победила пара 2

        attacker = agents[current_attacker]
        defender = agents[defending_team]
        attack_card = attacker.make_move(env, "attacker")

        if not attack_card:
            return 1 if current_attacker < 2 else 0

        defender_card = defender.make_move(env, "defender")
        if defender_card is None:  # Не смог отбить
            scores[defending_team // 2] += 1
            break
        else:
            env.move_to_discard_pile()  # Карты биты


# Статистика
strategies = [aggressive_strategy, enhanced_defensive_strategy, random_strategy, balanced_trap_strategy]

# Эксперименты
for agent1_strategy in strategies:
    for agent2_strategy in strategies:
        pair1_wins = 0
        pair2_wins = 0
        total_games = 1000  # 1000 игр
        for _ in range(total_games):
            result = play_game(agent1_strategy, agent2_strategy)
            if result == 0:
                pair1_wins += 1
            else:
                pair2_wins += 1

        # Вычисляем процент побед
        pair1_win_percentage = (pair1_wins / total_games) * 100
        pair2_win_percentage = (pair2_wins / total_games) * 100

        print(f"Стратегия Агентов 1: {agent1_strategy.__name__}, Стратегия Агентов 2: {agent2_strategy.__name__}")
        print(f"Пара 1 выиграла {pair1_win_percentage:.2f}%.")
        print(f"Пара 2 выиграла {pair2_win_percentage:.2f}%.")
        print("-" * 50)

