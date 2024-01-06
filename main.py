import os

import pygame
import pytmx

from Player import Hero
from Tile import Tile
from functoins import load_map
from login import login
from settings import *
from defeat import Defeat
from victory import Victory


# Инициализируем игру
pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
running = True
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
background_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
wall_group = pygame.sprite.Group()

full_tmx_path = os.path.join("data", NAME_MAP)
full_tileset_path = os.path.join("data", "Terrain (16x16).tsx")
map = pytmx.load_pygame(full_tmx_path, tileset=full_tileset_path)
map_array = load_map(full_tmx_path)
height = map.height
width = map.width

for y in range(height):
    for x in range(width):
        if x == 10 and y == 49:
            Tile(map, x, y, background_group)
            new_player = Hero(screen, HERO_IMAGE, player_group)
        elif map_array[y][x] == 1:
            Tile(map, x, y, wall_group)
        elif map_array[y][x] == 3 or map_array[y][x] == 2:
            Tile(map, x, y, background_group)

print(wall_group)

# "экран входа"
player_name = login()

is_jump = 0
game_over = False
game_won = False
target_direction = ""
print(map_array)

game_state = "playing"

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
            elif event.key == pygame.K_w:
                if not game_over and not game_won:
                    game_state = "defeat"
                    game_over = True

    if game_state == "defeat":
        defeat_screen = Defeat(WINDOW_WIDTH, WINDOW_HEIGHT)
        defeat_screen.display(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if defeat_screen.check_button_click(event):
                        game_state = "playing"
                        game_over = False

    elif game_state == "playing":
        if is_jump > 0:
            is_jump = new_player.move(target_direction, is_jump, wall_group)
            is_jump -= 1

        background_group.draw(screen)
        wall_group.draw(screen)
        player_group.draw(screen)

        wall_group.update()
        background_group.update()
        player_group.update()

        clock.tick(FPS)
        pygame.display.flip()

pygame.quit()