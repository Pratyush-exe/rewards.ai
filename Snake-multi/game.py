import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

pygame.init()


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


Point = namedtuple('Point', 'x, y')

# rgb colors
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)

BLOCK_SIZE = 20
SPEED = 40


class SnakeGameAI:

    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h

        self.head_1 = None
        self.head_2 = None
        self.head_3 = None

        self.snake_1 = []
        self.snake_2 = []
        self.snake_3 = []

        self.score_1 = 0
        self.score_2 = 0
        self.score_3 = 0

        self.direction_1 = None
        self.direction_2 = None
        self.direction_3 = None

        self.food = []
        self.frame_iteration = 0

        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        self.reset_1()
        self.reset_2()
        self.reset_3()
        self.food = []
        self._place_food()
        self.frame_iteration = 0

    def reset_1(self):
        self.direction_1 = Direction.RIGHT

        self.head_1 = Point(self.w / 2, self.h / 2)
        self.snake_1 = [self.head_1,
                        Point(self.head_1.x - BLOCK_SIZE, self.head_1.y),
                        Point(self.head_1.x - (2 * BLOCK_SIZE), self.head_1.y)]

        self.score_1 = 0

    def reset_2(self):
        self.direction_2 = Direction.RIGHT

        self.head_2 = Point(self.w / 2, self.h / 2)
        self.snake_2 = [self.head_2,
                        Point(self.head_2.x - BLOCK_SIZE, self.head_2.y),
                        Point(self.head_2.x - (2 * BLOCK_SIZE), self.head_2.y)]

        self.score_2 = 0

    def reset_3(self):
        self.direction_3 = Direction.RIGHT

        self.head_3 = Point(self.w / 2, self.h / 2)
        self.snake_3 = [self.head_3,
                        Point(self.head_3.x - BLOCK_SIZE, self.head_3.y),
                        Point(self.head_3.x - (2 * BLOCK_SIZE), self.head_3.y)]

        self.score_3 = 0

    def _place_food(self):
        if not self.food:
            for i in range(5):
                x = random.randint(0, (self.w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
                y = random.randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
                self.food.append(Point(x, y))

        for i, food in enumerate(self.food):
            if food in self.snake_1 + self.snake_2 + self.snake_3:
                x = random.randint(0, (self.w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
                y = random.randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
                self.food[i] = Point(x, y)

    def play_step(self, action):
        self.frame_iteration += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameOver1, self.score_1 = self.play_step_1(action[0])
        gameOver2, self.score_2 = self.play_step_2(action[1])
        gameOver3, self.score_3 = self.play_step_3(action[2])

        GAME_OVER = [gameOver1, gameOver2, gameOver3]
        SCORES = [self.score_1, self.score_2, self.score_3]

        self._update_ui()
        self.clock.tick(SPEED)

        return GAME_OVER, SCORES

    def play_step_1(self, action):
        self.direction_1, self.head_1 = self._move(action, self.direction_1, self.head_1)
        self.snake_1.insert(0, self.head_1)

        game_over = False
        if self.is_collision_1() or self.frame_iteration > 100 * len(self.snake_1):
            game_over = True
            return game_over, self.score_1

        eaten = False
        for food in self.food:
            if self.head_1 == food:
                eaten = True
                self.score_1 += 1
                self._place_food()
        if not eaten:
            self.snake_1.pop()

        return game_over, self.score_1

    def play_step_2(self, action):
        self.direction_2, self.head_2 = self._move(action, self.direction_2, self.head_2)
        self.snake_2.insert(0, self.head_2)

        game_over = False
        if self.is_collision_2() or self.frame_iteration > 100 * len(self.snake_2):
            game_over = True
            return game_over, self.score_2

        eaten = False
        for food in self.food:
            if self.head_2 == food:
                eaten = True
                self.score_2 += 1
                self._place_food()
        if not eaten:
            self.snake_2.pop()

        return game_over, self.score_2

    def play_step_3(self, action):
        self.direction_3, self.head_3 = self._move(action, self.direction_3, self.head_3)
        self.snake_3.insert(0, self.head_3)

        game_over = False
        if self.is_collision_3() or self.frame_iteration > 100 * len(self.snake_3):
            game_over = True
            return game_over, self.score_3

        eaten = False
        for food in self.food:
            if self.head_3 == food:
                eaten = True
                self.score_3 += 1
                self._place_food()
        if not eaten:
            self.snake_3.pop()

        return game_over, self.score_3

    def is_collision_1(self, pt=None):
        if pt is None:
            pt = self.head_1
        # hits boundary
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        # hits itself
        if pt in self.snake_1[1:]:
            return True

        return False

    def is_collision_2(self, pt=None):
        if pt is None:
            pt = self.head_2
        # hits boundary
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        # hits itself
        if pt in self.snake_2[1:]:
            return True

        return False

    def is_collision_3(self, pt=None):
        if pt is None:
            pt = self.head_3
        # hits boundary
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        # hits itself
        if pt in self.snake_3[1:]:
            return True

        return False

    def _update_ui(self):
        self.display.fill(BLACK)

        for snake in [self.snake_1, self.snake_2, self.snake_3]:
            for pt in snake:
                pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x + 4, pt.y + 4, 12, 12))

        for food in self.food:
            pygame.draw.rect(self.display, RED, pygame.Rect(food.x, food.y, BLOCK_SIZE, BLOCK_SIZE))

        pygame.display.flip()

    def _move(self, action, direction, head):
        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx]  # no change
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx]  # right turn r -> d -> l -> u
        else:  # [0, 0, 1]
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx]  # left turn r -> u -> l -> d

        direction = new_dir

        x = head.x
        y = head.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE

        head = Point(x, y)
        return direction, head
