from stable_baselines3 import PPO
import os
from testEnv import SnekEnv
import time
import gym
import numpy as np

models_dir = "models/%s/" % int(time.time())
logdir = "logs/%s/" % int(time.time())

if not os.path.exists(models_dir):
    os.makedirs(models_dir)

if not os.path.exists(logdir):
    os.makedirs(logdir)


def reward(props):
    euclidean_dist_to_apple = np.linalg.norm(np.array(props["snake_head"]) - np.array(props["apple_position"]))
    return euclidean_dist_to_apple


env = SnekEnv(reward_function=reward)
# env = gym.make("CartPole-v1")
env.reset()

model = PPO('MlpPolicy', env, verbose=1, tensorboard_log=logdir)

TIMESTEPS = 10000
iters = 0
while True:
    iters += 1
    model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name="PPO")
    model.save("%s/%s" % (models_dir, TIMESTEPS * iters))
