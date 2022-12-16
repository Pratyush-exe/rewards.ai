import torch
import random
import numpy as np
from collections import deque
import matplotlib.pyplot as plt

plt.ion()

MAX_MEMORY = 100_000
BATCH_SIZE = 1000


class Agent:
    def __init__(self, game, model, trainer):
        self.game = game
        self.n_games = 0
        self.epsilon = 0
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = model
        self.trainer = trainer
        self.play_trained = False

    def get_state(self, game):
        state = [
            game.head_body.position.x -
            game.base_body.position.x
        ]

        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_trained_action(self, state):
        final_move = [0, 0]
        state0 = torch.tensor(state, dtype=torch.float)
        prediction = self.model(state0)
        move = torch.argmax(prediction).item()
        final_move[move] = 1

        return final_move

    def get_action(self, state):
        self.epsilon = 20 - self.n_games
        final_move = [0, 0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 1)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move