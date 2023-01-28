import numpy as np
from game import Direction, Point


def get_state(snake, direction, is_collision, foods):
    head = snake[0]

    point_l = Point(head.x - 20, head.y)
    point_r = Point(head.x + 20, head.y)
    point_u = Point(head.x, head.y - 20)
    point_d = Point(head.x, head.y + 20)

    dir_l = direction == Direction.LEFT
    dir_r = direction == Direction.RIGHT
    dir_u = direction == Direction.UP
    dir_d = direction == Direction.DOWN

    foods_dist = [np.linalg.norm(np.array((head.x, head.y))-np.array((food.x, food.y))) for food in foods]
    index = np.argmin(foods_dist)

    state = [
        # Danger straight
        (dir_r and is_collision(point_r)) or
        (dir_l and is_collision(point_l)) or
        (dir_u and is_collision(point_u)) or
        (dir_d and is_collision(point_d)),

        # Danger right
        (dir_u and is_collision(point_r)) or
        (dir_d and is_collision(point_l)) or
        (dir_l and is_collision(point_u)) or
        (dir_r and is_collision(point_d)),

        # Danger left
        (dir_d and is_collision(point_r)) or
        (dir_u and is_collision(point_l)) or
        (dir_r and is_collision(point_u)) or
        (dir_l and is_collision(point_d)),

        # Move direction
        dir_l,
        dir_r,
        dir_u,
        dir_d,

        # Food location
        foods[index].x < head.x,  # food left
        foods[index].x > head.x,  # food right
        foods[index].y < head.y,  # food up
        foods[index].y > head.y  # food down
    ]

    return np.array(state, dtype=int)
