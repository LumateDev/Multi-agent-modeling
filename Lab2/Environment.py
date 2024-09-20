from Lab2.Agent import Agent
from Lab2.MessageBroker import MessageBroker
import random as rnd


class Environment:
    def __init__(self, agents_count):
        self.agents_count = agents_count
        self.agents = []
        self.patents_count = agents_count * 5
        for i in range(self.agents_count):
            agent = Agent(i + 1, [i for i in range(1, self.patents_count+1)], 5)
            agent.print_agent_description()
            self.agents.append(agent)

    def give_patents(self):
        patents = []
        for agent in self.agents:
            for patent in agent.target:
                patents.append(patent)
        print(f"All patents: {patents}")
        rnd.shuffle(patents)
        print(f"Shuffled patents: {patents}")
        patents_per_agent = len(patents) // self.agents_count
        for i in range(patents_per_agent):
            for agent in self.agents:
                patent = patents.pop(0)
                agent.get_patent(patent)
        for agent in self.agents:
            agent.print_agent_description()

    def simulate(self):
        broker = MessageBroker()
        iteration = 0
        while len([agent for agent in self.agents if len(agent.target) == len(agent.need_patents)]) != self.agents_count:
            iteration += 1

            print(f"Iteration: {iteration}")
            broker.communicate(self.agents)

            for agent in self.agents:
                if len(agent.target) != len(agent.need_patents):
                    agent.increase_count()
                agent.print_agent_description()

        for agent in self.agents:
            agent.increase_count()
            agent.print_results()
