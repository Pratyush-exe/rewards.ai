import pygame
from Player.Player import Player

pygame.init()

SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 500

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('SpriteSheets')

run = True
p1 = Player(screen, isRight=True)
last_update = pygame.time.get_ticks()
while run:
    screen.fill((0, 0, 0))
    current_time = pygame.time.get_ticks()
    if (current_time - last_update >= p1.idle_animation_cooldown and p1.idle) or \
            (current_time - last_update >= p1.walk_animation_cooldown and p1.walking):
        p1.update()
        last_update = current_time
    p1.draw()
    p1.move()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()
pygame.quit()
