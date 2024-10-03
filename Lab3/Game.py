import random


class Game:
    def __init__(self, agent, bot, court_size, grid_size, miss_chance=0.05):
        self.agent = agent
        self.bot = bot
        self.court_size = court_size
        self.grid_size = grid_size
        self.grid_step = court_size / grid_size
        self.miss_chance = miss_chance

    def serve(self):
        return [random.uniform(-self.court_size / 2, self.court_size / 2), random.uniform(0, self.court_size)]

    def bot_return(self, ball_position):
        return [-ball_position[0], self.court_size - ball_position[1]]

    def agent_hit(self, ball_position):
        target_x = -ball_position[0]
        target_y = self.court_size - ball_position[1]

        if random.random() < self.miss_chance:
            target_x += random.uniform(-self.grid_step, self.grid_step)
            target_y += random.uniform(-self.grid_step, self.grid_step)

        return [target_x, target_y]

    def simulate_point(self):
        """Симуляция одного розыгрыша"""
        ball_position = self.serve()
        print(f"Подача агента: {ball_position}")

        while True:
            if self.bot.can_hit(ball_position):
                ball_position = self.bot_return(ball_position)
                print(f"Болванчик отбил: {ball_position}")
            else:
                print(f"Болванчик не отбил, очко агенту!")
                return 1

            if self.agent.can_hit(ball_position):
                ball_position = self.agent_hit(ball_position)
                print(f"Агент отбил: {ball_position}")
            else:
                print(f"Агент не отбил, очко болванчику!")
                return 0
