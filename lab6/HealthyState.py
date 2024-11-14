from State import State


class HealthyState(State):
    def __init__(self, agent):
        super().__init__(agent)
        self.agent.speed = self.agent.base_speed

    def update(self):
        pass