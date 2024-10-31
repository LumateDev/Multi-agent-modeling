import networkx as nx
import matplotlib.pyplot as plt
import random
import time
from Module import *
from Agent import *


# Создание графа нагрузки с 20 модулями
def create_load_graph():
    G = nx.DiGraph()
    modules = [Module(i, random.uniform(0.5, 2.5)) for i in range(20)]

    for module in modules:
        G.add_node(module.id, load=module.load)

    # Добавляем увеличенное количество связей для повышения параллелизма
    edges = [
        (0, 1), (0, 2), (0, 3), (1, 4), (1, 5), (2, 6), (2, 7), (3, 8),
        (4, 9), (5, 10), (6, 11), (7, 12), (8, 13), (9, 14), (10, 15),
        (11, 16), (12, 17), (13, 18), (14, 19), (3, 14), (8, 15), (5, 17),
        (1, 18), (10, 12), (6, 19)
    ]
    G.add_edges_from(edges)

    return G, modules


# Создание графа агентов с 7 агентами
def create_agent_graph(num_agents=7):
    G = nx.Graph()
    agents = [Agent(i) for i in range(num_agents)]

    for agent in agents:
        G.add_node(agent.id)

    # Увеличиваем количество связей для более эффективного распределения нагрузки
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 0),
        (0, 3), (1, 4), (2, 5), (3, 6)  # Дополнительные связи
    ]
    G.add_edges_from(edges)

    return G, agents


# Начальное распределение нагрузки
def initial_distribution(modules, agents, load_graph):
    for agent in agents:
        if agent.active and agent.current_module is None:
            for module in modules:
                if module.state == "inactive":
                    predecessors = list(load_graph.predecessors(module.id))
                    if all(modules[p].state == "completed" for p in predecessors):
                        agent.assign_module(module)
                        break


# Перераспределение модулей от выбывшего агента соседним агентам
def redistribute_module_to_neighbors(agent, agent_graph, agents):
    module = agent.current_module
    if module and module.state == "active":
        neighbors = list(agent_graph.neighbors(agent.id))
        free_neighbor = next((agents[n] for n in neighbors if agents[n].active and agents[n].current_module is None),
                             None)

        if free_neighbor:
            free_neighbor.assign_module(module)
            print(f"Агент {agent.id} передал модуль {module.id} агенту {free_neighbor.id}")
        else:
            module.state = "inactive"
            print(f"Агент {agent.id} не смог передать модуль {module.id}, модуль возвращен в общий пул")


def visualize_graph(graph, title):
    pos = nx.spring_layout(graph)
    node_labels = {node: f"Модуль {node}" if graph.is_directed() else f"Агент {node}" for node in graph.nodes()}

    nx.draw(graph, pos, with_labels=True, node_color='lightblue', node_size=1000, font_size=12, font_color='black',
            font_weight='bold')
    plt.title(title)
    plt.xlabel("Модули и агенты")
    plt.ylabel("Состояние")

    for node in graph.nodes():
        plt.annotate(node_labels[node], xy=pos[node], textcoords="offset points", xytext=(0, 10), ha='center')

    plt.show()


def main():
    load_graph, modules = create_load_graph()
    agent_graph, agents = create_agent_graph(num_agents=7)

    print("Граф нагрузки:")
    visualize_graph(load_graph, "Граф нагрузки")

    print("Граф агентов:")
    visualize_graph(agent_graph, "Граф агентов")

    initial_distribution(modules, agents, load_graph)

    time_start = time.time()

    while any(module.state != "completed" for module in modules):
        for agent in agents:
            if agent.active and agent.current_module and agent.current_module.state == "active":
                print(
                    f"Агент {agent.id} выполняет модуль {agent.current_module.id} с нагрузкой {agent.current_module.load:.2f}")
                time.sleep(agent.current_module.load)

                if random.random() < 0.05:
                    agent.fail()
                    redistribute_module_to_neighbors(agent, agent_graph, agents)
                    continue

                completed_module = agent.complete_module()
                print(f"Агент {agent.id} завершил модуль {completed_module.id} с нагрузкой {completed_module.load:.2f}")

        for agent in agents:
            if agent.active and agent.current_module is None:
                initial_distribution(modules, agents, load_graph)

    total_time = time.time() - time_start
    print(f"Общее время выполнения приложения: {total_time:.2f} секунд")


if __name__ == "__main__":
    main()
