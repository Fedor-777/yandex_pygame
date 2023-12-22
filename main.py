import pygame

from Player import Hero
from level import Level
from login import login
from settings import *

# Инициализируем игру
pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
running = True
clock = pygame.time.Clock()

login()
pos_x = 200
pos_y = 600
level = Level("безымянный.tmx", [23], 117)
hero = Hero(screen, "data/box.png", pos_x, pos_y, "data/безымянный.tmx")

is_jump = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                target_direction = "a"
                is_jump = LEN_JUMP
            elif event.key == pygame.K_d:
                target_direction = "d"
                is_jump = LEN_JUMP
    if is_jump > 0:
        hero.move(target_direction, is_jump)
        is_jump -= 1

    screen.fill(pygame.Color("black"))
    level.render(screen)
    screen.blit(hero.image, hero.rect)

    clock.tick(FPS)
    pygame.display.flip()

pygame.quit()
