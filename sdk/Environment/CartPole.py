import pygame
import pymunk
import random
import math

pygame.init()


def convert_points(point):
    return int(point[0]), int(point[1])


class Game:
    def __init__(self, reward_function, game_over_condition, train=True):
        self.display = pygame.display.set_mode((600, 600))
        self.train = train
        self.reward_function = reward_function
        self.game_over_condition = game_over_condition

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

        self.angle = self.get_angle()

        self.space.add(self.head_body, self.head_shape)
        self.space.add(self.joint)

    def get_angle(self):
        basex, basey = self.base_body.position
        headx, heady = self.head_body.position
        angle = math.atan((heady - basey) / (headx - basex))
        return math.degrees(angle)

    def check_failed(self):
        self.GameOver = self.game_over_condition({
            "head_body_position": self.head_body.position,
            "base_body_position": self.base_body.position,
            "base_stick_angle": self.get_angle()
        })

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
        if not self.train:
            keys = pygame.key.get_pressed()
            X, Y = self.base_body.position
            if keys[pygame.K_RIGHT]:
                X += self.speed
                self.base_body.position = X, Y
            elif keys[pygame.K_LEFT]:
                X -= self.speed
                self.base_body.position = X, Y
        else:
            X, Y = self.base_body.position
            if action[0] > action[1]:
                X += self.speed
                self.base_body.position = X, Y
            elif action[1] > action[0]:
                X -= self.speed
                self.base_body.position = X, Y
            else:
                pass

    def play_Step(self, action):
        self.iterations += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        self.move(action)
        self.draw()

        self.check_failed()

        if abs(self.score) > 250:
            self.GameOver = True

        reward = self.reward_function({
            "game_over_status": self.GameOver,
            "base_body_position": self.base_body.position,
            "base_stick_angle": self.get_angle()
        })

        self.score += reward

        self.timeTicking()
        return reward, self.GameOver, self.score
