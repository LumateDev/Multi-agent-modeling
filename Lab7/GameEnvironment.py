from Card import *
import random
from collections import deque

class GameEnvironment:
    def __init__(self):
        suits = ['♠', '♣', '♥', '♦']
        ranks = list(range(6, 15))
        self.deck = deque([Card(suit, rank) for suit in suits for rank in ranks])
        random.shuffle(self.deck)
        self.discard_pile = []
        self.hands = {i: [] for i in range(4)}
        self.table = []
        self.trump = None

    def deal(self):
        self.trump = self.deck[-1]
        for _ in range(6):
            for i in range(4):
                if self.deck:
                    self.hands[i].append(self.deck.popleft())

    def reset_table(self):
        self.table = []

    def move_to_discard_pile(self):
        self.discard_pile.extend(self.table)
        self.reset_table()