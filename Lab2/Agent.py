from collections import Counter
import random as rnd


class Agent:
    def __init__(self, agent_id, target_numbers, count_target_task):
        self.id = agent_id
        self.target = sorted(rnd.sample(target_numbers, count_target_task))
        self.need_patents = []
        self.tradable_patents = []
        self.iterations_count = 0
        self.communications_count = 0

    @property
    def get_tradable_patents(self):
        return self.tradable_patents

    def print_agent_description(self):
        missing_need_patents = self.get_need_patents()
        missing_need_patents_list = []
        for k, v in missing_need_patents.items():
            missing_need_patents_list.extend([k] * v)
        missing_need_patents_list = sorted(missing_need_patents_list)
        print(
            f"Agent {self.id}, target: {self.target} collected {self.need_patents} can trade {self.tradable_patents} need {missing_need_patents_list}"
        )

    def print_results(self):
        print(
            f"Agent {self.id} finish collecting target {self.target} in {self.iterations_count} iterations and {self.communications_count} communications"
        )

    def change(self, patent):
        self.communications_count += 1
        self.get_patent(patent)

    def get_patent(self, patent):
        count_patent = self.target.count(patent)
        if count_patent > 0 and self.need_patents.count(patent) < count_patent:
            self.need_patents.append(patent)
            self.need_patents = sorted(self.need_patents)
        else:
            self.tradable_patents.append(patent)
            self.tradable_patents = sorted(self.tradable_patents)

    def increase_count(self):
        self.iterations_count += 1

    def get_need_patents(self):
        target_patent_count = Counter(self.target)
        collected_patent_count = Counter(self.need_patents)
        missing_patents = {}
        for patent, target_count in target_patent_count.items():
            collected_count = collected_patent_count.get(patent, 0)
            if collected_count < target_count:
                missing_patents[patent] = target_count - collected_count
        return missing_patents

    def check_all_targets(self):
        return dict(Counter(self.target)) == dict(Counter(self.need_patents))
