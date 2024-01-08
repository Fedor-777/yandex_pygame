import os

import pygame
import pytmx

from Player import Hero
from Tile import Tile
from functoins import load_map, load_image
from login import login
from settings import *
from defeat import defeat
from victory import victory

def main_screen():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    clock = pygame.time.Clock()

    background_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    wall_group = pygame.sprite.Group()
    finish_group = pygame.sprite.Group()

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
                new_player = Hero(screen, player_group)
            elif map_array[y][x] == 1 or map_array[y][x] == 3 or map_array[y][x] == 6 or map_array[y][x] == 4 or \
                    map_array[y][x] == 7:
                Tile(map, x, y, wall_group)
            elif map_array[y][x] == 5:
                Tile(map, x, y, background_group)
            elif map_array[y][x] == 2:
                Tile(map, x, y, finish_group)

    running = True

    is_jump = 0
    game_over = False
    game_won = False
    target_direction = ""
    screen.fill((0, 0, 0))
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

        finish_collisions = pygame.sprite.spritecollide(new_player, finish_group, False)
        if finish_collisions:
            repeat = victory(screen, clock)
            is_jump = 0
            if repeat:
                new_player.rect.x = 300
                new_player.rect.y = 1180
                # print(new_player)
            else:
                running = False
        else:
            if is_jump > 0:
                is_jump = new_player.move(target_direction, is_jump, wall_group)
                is_jump -= 1

            screen.fill((0, 0, 0))
            background_group.draw(screen)
            wall_group.draw(screen)
            finish_group.draw(screen)
            player_group.draw(screen)

            player_group.update()
            clock.tick(FPS)
            pygame.display.flip()