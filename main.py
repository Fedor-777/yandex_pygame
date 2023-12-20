import pygame

from login import login
import pytmx
from level import Level
from settings import *
from Player import Hero

# Инициализируем игру
pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
running = True
clock = pygame.time.Clock()


login()
pos_x = 2
pos_y = 1
level = Level("безымянный.tmx", [23], 117)
hero = Hero("data/box.png", pos_x, pos_y, "data/безымянный.tmx")

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                hero.move("w")
            if event.key == pygame.K_s:
                hero.move("s")
            if event.key == pygame.K_a:
                hero.move("a")
            if event.key == pygame.K_d:
                hero.move("d")


    screen.fill(pygame.Color("black"))
    level.render(screen)
    # Отрисовываем игрока
    hero_rect = hero.rect
    screen.blit(hero.image, hero_rect)

    clock.tick(FPS)
    pygame.display.flip()
pygame.quit()
