from game import SnakeGameAI
from agent import get_state
from model import Linear_QNet, QTrainer
import matplotlib.pyplot as plt
import pygame
import time
import torch

plt.ion()

OUTPUT = 3

plot_scores = []
plot_mean_scores = []
total_score = 0
record = 0

model_1 = Linear_QNet(11, 256, 3)
model_1.load_state_dict(torch.load("model/model.pth"))
model_1.eval()

model_2 = Linear_QNet(11, 256, 3)
model_2.load_state_dict(torch.load("model/model_1.pth"))
model_2.eval()

model_3 = Linear_QNet(11, 256, 3)
model_3.load_state_dict(torch.load("model/model.pth"))
model_3.eval()

game = SnakeGameAI()
prev_dir = None

while True:
    time.sleep(0.05)
    pygame.display.update()

    snake1 = game.snake_1
    snake2 = game.snake_2
    snake3 = game.snake_3

    action = [[0 for i in range(OUTPUT)],
              [0 for i in range(OUTPUT)],
              [0 for i in range(OUTPUT)]]

    res_1 = model_1(torch.tensor(get_state(game.snake_1, game.direction_1, game.is_collision_1, game.food), dtype=torch.float))
    res_2 = model_2(torch.tensor(get_state(game.snake_2, game.direction_2, game.is_collision_2, game.food), dtype=torch.float))
    res_3 = model_3(torch.tensor(get_state(game.snake_3, game.direction_3, game.is_collision_3, game.food), dtype=torch.float))

    action[0][torch.argmax(res_1).item()] = 1
    action[1][torch.argmax(res_2).item()] = 1
    action[2][torch.argmax(res_3).item()] = 1

    GAME_OVER, _ = game.play_step(action)
    if GAME_OVER[0]: game.reset_1()
    if GAME_OVER[1]: game.reset_2()
    if GAME_OVER[2]: game.reset_3()
