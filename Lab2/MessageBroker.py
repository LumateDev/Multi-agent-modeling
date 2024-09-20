from collections import Counter


class MessageBroker:

    def get_new_tradable_patents(self, agents, tradable_patents):
        for agent in agents:
            patents = agent.tradable_patents
            for i in range(len(tradable_patents)):

                if tradable_patents[i] != dict(Counter(patents)):
                    tradable_patents[i] = dict(Counter(patents))

        return tradable_patents

    def communicate(self, agents):

        tradable_patents = []
        tradable = False
        for agent in agents:
            patents_count = Counter(agent.get_tradable_patents)
            tradable_patents.append(dict(patents_count))

        for agent in agents:
            agent_missing_patent = agent.get_need_patents()

            for other_agent in agents:
                if agent.id != other_agent.id:
                    if any(patent in other_agent.tradable_patents for patent in
                           agent_missing_patent):
                        other_agent_missing_patents = other_agent.get_need_patents()
                        if any(patent in agent.tradable_patents for patent in
                               other_agent_missing_patents):
                            self.trade(agent, other_agent)
                            tradable_patents = self.get_new_tradable_patents(agents, tradable_patents)
                            tradable = True
                            break
        if not tradable:
            for agent in agents:
                if not agent.check_all_targets():
                    print(
                        f"For agent {agent.id} direct exchange is not possible, looking for a chain of exchanges")
                    self.find_chain(agents, agent.id - 1, tradable_patents)

    def trade(self, first_agent, second_agent):

        first_patent = 0
        for patent in first_agent.tradable_patents:
            if patent in second_agent.get_need_patents():
                first_agent.tradable_patents.remove(patent)
                second_agent.change(patent)
                first_patent = patent
                break
        second_patent = 0
        for patent in second_agent.tradable_patents:
            if patent in first_agent.get_need_patents():
                second_agent.tradable_patents.remove(patent)
                first_agent.change(patent)
                second_patent = patent
                break
        print(f"Agents {first_agent.id} <--> {second_agent.id} exchanged patents {first_patent} <--> {second_patent}")
        first_agent.print_agent_description()
        second_agent.print_agent_description()

    def find_chain(self, list_of_agents: list, i: int, list_of_all_tradable_patents: list):
        print(f"search for a chain for the agent begins {list_of_agents[i].id}")
        current_agent = list_of_agents[i]
        path = [list_of_agents[i].id]
        visited_agents = []
        new_current_agent = self.find_link(list_of_agents, current_agent, path,
                                           visited_agents)
        while path[0] != path[-1]:
            if new_current_agent != None:
                new_current_agent = self.find_link(list_of_agents, new_current_agent, path,
                                                   visited_agents)
            else:
                print(f"Chain for agent {current_agent} not formed")
                return None
        print(f"Find path: {path}")
        self.trade_chain(list_of_agents, path, list_of_all_tradable_patents)

    def find_link(self, list_of_agents, current_agent, path, visited_agents):
        for useless_patent in current_agent.tradable_patents:
            for i in range(len(list_of_agents)):
                if list_of_agents[i] != current_agent and list_of_agents[i] not in visited_agents:
                    if useless_patent in list_of_agents[i].get_need_patents():
                        path.append(list_of_agents[i].id)
                        visited_agents.append(list_of_agents[i])
                        print(f"Next agent for chain: {list_of_agents[i].id}")
                        return list_of_agents[i]
        return None

    def trade_chain(self, agents, path, tradable_patents):
        for i in range(len(path) - 1):
            for j in range(len(agents)):
                if agents[j].id == path[i]:
                    useless_patent = agents[j].tradable_patents[0]
                    agents[j].tradable_patents.remove(useless_patent)
                    for k in range(len(agents)):
                        if agents[k].id == path[i + 1]:
                            agents[k].change(useless_patent)
                            print(f"Agent {agents[j].id} gave {useless_patent} to Agent {agents[k].id}")
                            agents[i].print_agent_description()
                            agents[k].print_agent_description()
                            tradable_patents = self.get_new_tradable_patents(agents, tradable_patents)
