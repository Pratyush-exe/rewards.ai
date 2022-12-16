import torch
import random
import numpy as np
from collections import deque
import matplotlib.pyplot as plt

plt.ion()

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001


def plot(scores, mean_scores):
    plt.clf()
    plt.title('Training...')
    plt.xlabel('Number of Games')
    plt.ylabel('Score')
    plt.plot(scores)
    plt.plot(mean_scores)
    plt.ylim(ymin=0)
    plt.text(len(scores) - 1, scores[-1], str(scores[-1]))
    plt.text(len(mean_scores) - 1, mean_scores[-1], str(mean_scores[-1]))
    plt.show(block=False)
    plt.pause(.1)


def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    if agent.play_trained:
        agent.model.load()
    game = BalanceStick()
    while True:
        state_old = agent.get_state(game)
        if not agent.play_trained:
            final_move = agent.get_action(state_old)
        else:
            final_move = agent.get_trained_action(state_old)
        reward, done, score = game.play_Step(final_move)
        if not agent.play_trained:
            state_new = agent.get_state(game)
            agent.train_short_memory(state_old, final_move, reward, state_new, done)
            agent.remember(state_old, final_move, reward, state_new, done)
        game.timeTicking()

        if done:
            game.initialize()
            agent.n_games += 1
            if agent.play_trained:
                print('Game', agent.n_games, 'Score', score)
            else:
                agent.train_long_memory()
                if score > record:
                    record = score
                    agent.model.save()
                print('Game', agent.n_games, 'Score', score, 'Record:', record)

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)


if __name__ == '__main__':
    train()
