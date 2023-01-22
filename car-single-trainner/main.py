from game import CarSingle
from model import Linear_QNet, QTrainer
import matplotlib.pyplot as plt
from agent import Agent
import pygame
import time

plt.ion()

MODE = "human"  # human, training, trained


def func(props):
    reward = 0
    if props["isAlive"]:
        reward = 1
    obs = props["obs"]
    if obs[0] < obs[-1] and props["dir"] == -1:
        reward += 1
    elif obs[0] > obs[-1] and props["dir"] == 1:
        reward += 1
    else:
        reward += 0
    return reward


plot_scores = []
plot_mean_scores = []
total_score = 0
record = 0
agent = Agent()
if agent.play_trained:
    agent.model.load()
game = CarSingle(func)

while True:
    if MODE == "human":
        time.sleep(0.05)
        pygame.display.update()
        action = [0, 0, 0, 0, 0, 0]
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            action[0] = 1
        elif keys[pygame.K_d]:
            action[1] = 1
        elif keys[pygame.K_w]:
            action[2] = 1
        elif keys[pygame.K_1]:
            action[3] = 1
        elif keys[pygame.K_2]:
            action[4] = 1
        elif keys[pygame.K_3]:
            action[5] = 1
        reward, done, score = game.play_Step(action)
    else:
        pygame.display.update()
        game.FPS = 20
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

            plt.clf()
            plt.title('Training...')
            plt.xlabel('Number of Games')
            plt.ylabel('Score')
            plt.plot(plot_scores)
            plt.plot(plot_mean_scores)
            plt.ylim(ymin=0)
            plt.text(len(plot_scores) - 1, plot_scores[-1], str(plot_scores[-1]))
            plt.text(len(plot_mean_scores) - 1, plot_mean_scores[-1], str(plot_mean_scores[-1]))
            plt.show(block=False)
            plt.pause(.1)
