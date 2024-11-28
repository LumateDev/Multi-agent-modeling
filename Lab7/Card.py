class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __repr__(self):
        return f"{self.rank}{self.suit}"

    def __lt__(self, other):
        if self.suit == other.suit:
            return self.rank < other.rank
        return False