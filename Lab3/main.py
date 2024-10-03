import matplotlib.pyplot as plt
import numpy as np

from Lab3.Game import Game
from Lab3.Player import Player


def simulate_game(agent, bot, court_size, grid_size, games=100):
    agent_wins = 0
    game = Game(agent, bot, court_size, grid_size)

    for _ in range(games):
        result = game.simulate_point()
        agent_wins += result

    return agent_wins / games


def plot_probability_vs_params():
    court_size = 8
    grid_size_range = range(3, 11)
    radius_range = np.linspace(1, 5, 10)
    probabilities = np.zeros((len(grid_size_range), len(radius_range)))

    agent = Player("Агент", radius=2, move_range=1)
    bot = Player("Болванчик", radius=1, move_range=1)

    for i, grid_size in enumerate(grid_size_range):
        for j, radius in enumerate(radius_range):
            agent.radius = radius
            win_prob = simulate_game(agent, bot, court_size, grid_size)
            probabilities[i, j] = win_prob
            print(f"Размер корта: {grid_size}, Радиус: {radius}, Вероятность победы: {win_prob}")

    X, Y = np.meshgrid(grid_size_range, radius_range)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, probabilities.T, cmap='viridis')
    ax.set_xlabel('Размер корта')
    ax.set_ylabel('Радиус')
    ax.set_zlabel('Вероятность победы')
    plt.show()


plot_probability_vs_params()
