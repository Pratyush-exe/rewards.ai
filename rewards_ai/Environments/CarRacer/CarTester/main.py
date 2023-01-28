from game import gameController, Car
from model import Linear_QNet, QTrainer
import matplotlib.pyplot as plt
import pygame
import time
import torch

plt.ion()

MODE = "training"  # human, training, trained
OUTPUT = 3


plot_scores = []
plot_mean_scores = []
total_score = 0
record = 0

car_1 = Car()
model_1 = Linear_QNet(5, 16, OUTPUT)
model_1.load_state_dict(torch.load("model/model.pth"))
model_1.eval()

car_2 = Car()
model_2 = Linear_QNet(5, 16, OUTPUT)
model_2.load_state_dict(torch.load("model/model_2.pth"))
model_2.eval()

car_3 = Car()
model_3 = Linear_QNet(5, 16, OUTPUT)
model_3.load_state_dict(torch.load("model/model.pth"))
model_3.eval()

game = gameController(car_1, car_2, car_3)

while True:
    time.sleep(0.05)
    pygame.display.update()
    action = [[0 for i in range(OUTPUT)],
              [0 for i in range(OUTPUT)],
              [0 for i in range(OUTPUT)]]

    res_1 = model_1(torch.tensor(car_1.radars, dtype=torch.float))
    res_2 = model_2(torch.tensor(car_2.radars, dtype=torch.float))
    res_3 = model_3(torch.tensor(car_3.radars, dtype=torch.float))

    action[0][torch.argmax(res_1).item()] = 1
    action[1][torch.argmax(res_2).item()] = 1
    action[2][torch.argmax(res_3).item()] = 1

    game.play_Step(action)
    if not game.alive:
        game.initialize()
