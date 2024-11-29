import random


# Агрессивная стратегия: при атаке выбирает самую сильную карту, при защите — минимально возможную для отражения.
def aggressive_strategy(agent, env, role):
    if role == "attacker":
        return max(agent.hand, key=lambda x: x.rank)
    elif role == "defender":
        attacking_card = env.table[-1]
        valid_moves = [card for card in agent.hand if card.suit == attacking_card.suit and card.rank > attacking_card.rank]
        return min(valid_moves, key=lambda x: x.rank, default=None)


# Защитная стратегия: минимизирует потери, играя слабейшей возможной картой.
def defensive_strategy(agent, env, role):
    if role == "attacker":
        return min(agent.hand, key=lambda x: x.rank)
    elif role == "defender":
        attacking_card = env.table[-1]
        valid_moves = [card for card in agent.hand if card.suit == attacking_card.suit and card.rank > attacking_card.rank]
        return max(valid_moves, key=lambda x: x.rank, default=None)


# Случайная стратегия: хаотичное поведение.
def random_strategy(agent, env, role):
    return random.choice(agent.hand) if agent.hand else None


# Стратегия баланса: при атаке использует карты средней силы.
def balanced_strategy(agent, env, role):
    if role == "attacker":
        return sorted(agent.hand, key=lambda x: x.rank)[len(agent.hand) // 2]
    elif role == "defender":
        attacking_card = env.table[-1]
        valid_moves = [card for card in agent.hand if card.suit == attacking_card.suit and card.rank > attacking_card.rank]
        return sorted(valid_moves, key=lambda x: x.rank)[len(valid_moves) // 2] if valid_moves else None
