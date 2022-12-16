from sdk.Environment import CartPole
from sdk.agent import Agent
from sdk.Player import Player
from sdk.train_utils import Default_QNet, Trainer


# reward function
def reward(state):
    reward = 0
    if abs(state["base_stick_angle"]) >= 80:
        reward = 1
    elif abs(state["base_stick_angle"]) <= 0:
        reward = -1
    return reward


# reset condition
def reset_condition(state):
    if state["head_body_position"].y > 350 or \
            0 > state["base_body_position"].x or \
            state["base_body_position"].x > 600:
        GameOver = True
    else:
        GameOver = False
    return GameOver


# game = CartPole.Game(reward, reset_condition, train=False)
game = CartPole.Game(reward, reset_condition, train=True)
model = Default_QNet()
trainer = Trainer(model)
agent = Agent(game, model, trainer)
player = Player(agent, game)

player.play()
