import numpy as np


class Player:
    def __init__(self, name, radius, move_range):
        self.name = name
        self.position = [0, 0]
        self.radius = radius
        self.move_range = move_range

    def move_to(self, target_position):
        """Перемещаемся к цели, если это возможно"""
        dx = target_position[0] - self.position[0]
        dy = target_position[1] - self.position[1]
        distance = np.sqrt(dx ** 2 + dy ** 2)
        if distance <= self.move_range:
            self.position = target_position
        else:
            factor = self.move_range / distance
            self.position[0] += dx * factor
            self.position[1] += dy * factor

    def can_hit(self, ball_position):
        """Проверяем, попадает ли мяч в радиус действия"""
        dx = ball_position[0] - self.position[0]
        dy = ball_position[1] - self.position[1]
        distance = np.sqrt(dx ** 2 + dy ** 2)
        return distance <= self.radius
