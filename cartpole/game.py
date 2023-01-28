import pygame
import pymunk
import random

pygame.init()


def convert_points(point):
    return int(point[0]), int(point[1])


class BalanceStick:
    def __init__(self):
        self.display = pygame.display.set_mode((600, 600))

        self.FPS = 60
        self.iterations = 0
        self.speed = 5

        self.initialize()

    def initialize(self):
        xpos = random.randint(298, 302)
        while xpos == 300:
            xpos = random.randint(298, 302)

        self.GameOver = False
        self.score = 0
        self.clock = pygame.time.Clock()

        self.space = pymunk.Space()
        self.space.gravity = (0, 1000)
        self.space.damping = 0.8

        self.base_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.base_body.position = 300, 300

        self.head_body = pymunk.Body()
        self.head_body.position = xpos, 100
        self.head_shape = pymunk.shapes.Circle(self.head_body, 10)
        self.head_shape.elasticity = 1
        self.head_shape.density = 1
        self.joint = pymunk.PinJoint(self.head_body, self.base_body)

        self.space.add(self.head_body, self.head_shape)
        self.space.add(self.joint)

        # return [self.head_body.position.x - self.base_body.position.x], 0, self.GameOver

    def check_failed(self):
        if self.head_body.position.y > 350 or 0 > self.base_body.position.x or self.base_body.position.x > 600:
            self.GameOver = True
        else:
            self.GameOver = False

    def draw(self):
        self.display.fill((255, 255, 255))
        pygame.draw.circle(self.display, (0, 0, 0), convert_points(self.base_body.position), 10)
        pygame.draw.line(self.display, (255, 0, 0), convert_points(self.head_body.position),
                         convert_points(self.base_body.position), 3)
        pygame.draw.line(self.display, (0, 0, 0), (0, 300), (600, 300), 1)
        pygame.display.update()

    def timeTicking(self):
        self.clock.tick(self.FPS)
        self.space.step(1 / self.FPS)

    def move(self, action):
        X, Y = self.base_body.position
        if action[0] > action[1]:
            X += self.speed
            self.base_body.position = X, Y
        elif action[1] > action[0]:
            X -= self.speed
            self.base_body.position = X, Y
        else:
            pass

        # For PolicyGradientAlgo
        # X, Y = self.base_body.position
        #
        # if action == 1:
        #     X += self.speed
        #     self.base_body.position = X, Y
        # elif action == 0:
        #     X -= self.speed
        #     self.base_body.position = X, Y

    def play_Step(self, action):
        self.iterations += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        self.move(action)
        self.draw()

        reward = 0
        self.check_failed()

        # For RandomPolicyAgent
        if self.score > 200:
            self.GameOver = True

        if self.GameOver:
            reward = 0
            self.score += reward
        else:
            if self.iterations > 0:
                reward = 1
                self.score += reward

        self.timeTicking()
        return reward, self.GameOver, self.score

        # For 3_LinearEstimator
        # state = [self.head_body.position.x - self.base_body.position.x]
        # return state, reward, self.GameOver

        # keys = pygame.key.get_pressed()
        # X, Y = self.base_body.position
        # if keys[pygame.K_RIGHT]:
        #     X += self.speed
        #     self.base_body.position = X, Y
        # elif keys[pygame.K_LEFT]:
        #     X -= self.speed
        #     self.base_body.position = X, Y

# if __name__ == '__main__':
#     game = Not_Let_It_Fall()
#     clock = pygame.time.Clock()
#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 break
#         game.play_Step()
#         if game.head_body.position.y > 350:
#             game.initialize()
#         game.draw()
#         clock.tick(game.FPS)
#         game.space.step(1 / game.FPS)
