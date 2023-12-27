import os

import pygame
import pytmx

from Player import Hero
from Tile import Tile
from functoins import load_map
from login import login
from settings import *

# Инициализируем игру
pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
running = True
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

full_tmx_path = os.path.join("data", NAME_MAP)
full_tileset_path = os.path.join("data", "Terrain (16x16).tsx")
map = pytmx.load_pygame(full_tmx_path, tileset=full_tileset_path)
map_array = load_map(full_tmx_path)
height = map.height
width = map.width

for y in range(height):
    for x in range(width):
        # print(x, y)
        if x == 10 and y == 49:
            Tile(map, x, y, tiles_group)
            new_player = Hero(screen, HERO_IMAGE, x, y, player_group)
        elif map_array[y][x] == 3 or map_array[y][x] == 2 or map_array[y][x] == 1 or map_array[y][x] == 4:
            Tile(map, x, y, tiles_group)

login()

is_jump = 0
print(new_player)
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
        new_player.move(target_direction, is_jump)
        is_jump -= 1

    screen.fill(pygame.Color("black"))
    tiles_group.draw(screen)
    player_group.draw(screen)
    player_group.update()  # Перемещаем эту строку вниз

    clock.tick(FPS)
    pygame.display.flip()

pygame.quit()