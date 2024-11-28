class Agent:
    def __init__(self, id, strategy):
        self.id = id
        self.strategy = strategy
        self.hand = []

    def make_move(self, env, role, partner_hand=None):
        if not self.hand:
            return None
        return self.strategy(self, env, role, partner_hand)