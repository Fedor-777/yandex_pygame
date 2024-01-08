import os
import time

import pygame
import pygame_gui
import pytmx

from Player import Hero
from Tile import Tile
from functoins import load_map
from settings import *


def main_screen(name_map):
    pygame.init()
    start_time = time.time()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    clock = pygame.time.Clock()

    background_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    wall_group = pygame.sprite.Group()
    finish_group = pygame.sprite.Group()
    obstacles_group = pygame.sprite.Group()

    full_tmx_path = os.path.join("data", name_map)
    # full_tileset_path = os.path.join("data", "Terrain (16x16).tsx")
    map = pytmx.load_pygame(full_tmx_path)
    map_array = load_map(full_tmx_path)
    height = map.height
    width = map.width

    for y in range(height):
        for x in range(width):
            if x == 10 and y == 49:
                Tile(map, x, y, background_group)
                new_player = Hero(screen, player_group)
            elif map_array[y][x] == 1 or map_array[y][x] == 3 or map_array[y][x] == 6 or map_array[y][x] == 4 or \
                    map_array[y][x] == 8:
                Tile(map, x, y, wall_group)
            elif map_array[y][x] == 5:
                Tile(map, x, y, background_group)
            elif map_array[y][x] == 2:
                Tile(map, x, y, finish_group)
            elif map_array[y][x] == 7 or map_array[y][x] == 9:
                Tile(map, x, y, obstacles_group)

    running = True

    is_jump = 0
    target_direction = ""
    screen.fill((0, 0, 0))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a and is_jump <= 0:
                    target_direction = "a"
                    is_jump = LEN_JUMP
                elif event.key == pygame.K_d and is_jump <= 0:
                    target_direction = "d"
                    is_jump = LEN_JUMP
                elif event.key == pygame.K_r:
                    end_time = time.time()
                    elapsed_time = end_time - start_time
                    victory(screen, elapsed_time, name_map[-5])
                    is_jump = 0
                    running = False

        finish_collisions = pygame.sprite.spritecollide(new_player, finish_group, False)
        defeat_collisions = pygame.sprite.spritecollide(new_player, obstacles_group, False)

        if finish_collisions:
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(elapsed_time)
            victory(screen, elapsed_time, name_map[-5])
            is_jump = 0
            running = False
        elif defeat_collisions:
            defeat(screen, clock, name_map)
            is_jump = 0
            running = False
        else:
            if is_jump > 0:
                is_jump = new_player.move(target_direction, is_jump, wall_group)
                is_jump -= 1
            else:
                if new_player.rect.y < 1180:
                    new_player.rect.move_ip(0, 2)

            screen.fill((0, 0, 0))
            background_group.draw(screen)
            wall_group.draw(screen)
            finish_group.draw(screen)
            obstacles_group.draw(screen)
            player_group.draw(screen)

            player_group.update()
            clock.tick(FPS)
            pygame.display.flip()

    pygame.quit()


def level(screen, clock):
    manager = pygame_gui.UIManager((800, 600))
    is_running = True
    screen.fill((0, 0, 255))

    first_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((150, 200), (50, 50)),
                                                text='1',
                                                manager=manager)

    second_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((200, 200), (50, 50)),
                                                 text='2',
                                                 manager=manager)
    third_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 200), (50, 50)),
                                                text='3',
                                                manager=manager)
    fourth_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((150, 255), (50, 50)),
                                                 text='4',
                                                 manager=manager)
    fifth_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((200, 255), (50, 50)),
                                                text='5',
                                                manager=manager)
    sixth_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 255), (50, 50)),
                                                text='6',
                                                manager=manager)

    while is_running:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == first_button:
                    main_screen("уровень1.tmx")
                elif event.ui_element == second_button:
                    main_screen("уровень2.tmx")
                elif event.ui_element == third_button:
                    main_screen("уровень3.tmx")
                elif event.ui_element == fourth_button:
                    main_screen("уровень4.tmx")
                elif event.ui_element == fifth_button:
                    main_screen("уровень5.tmx")
                elif event.ui_element == sixth_button:
                    main_screen("уровень6.tmx")

            manager.process_events(event)

        manager.update(time_delta)
        manager.draw_ui(screen)

        pygame.display.update()
    pygame.quit()


def victory(screen, elapsed_time, number_of_lvl):
    manager = pygame_gui.UIManager((800, 600))
    font = pygame.font.Font(None, 32)
    color = pygame.Color('dodgerblue2')
    clock = pygame.time.Clock()
    is_running = True

    screen.fill((0, 255, 0))
    number_of_lvl = int(elapsed_time)
    if number_of_lvl == 2 or number_of_lvl == 3 or number_of_lvl == 4:
        txt_surface = font.render("поздравляем, вы прошли уровень " + f"{number_of_lvl} за {number_of_lvl} секунды",
                                  True, color)
    else:
        txt_surface = font.render("поздравляем, вы прошли уровень " + f"{number_of_lvl} за {number_of_lvl} секунд",
                                  True, color)

    screen.blit(txt_surface, (50, 200))
    win = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((225, 550), (175, 50)),
                                       text='Выбрать уровень',
                                       manager=manager)

    while is_running:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == win:
                    # elapsed_time
                    level(screen, clock)

            manager.process_events(event)

        manager.update(time_delta)
        manager.draw_ui(screen)

        pygame.display.update()
    pygame.quit()


def defeat(screen, clock, name_map):
    manager = pygame_gui.UIManager((800, 1000))
    font = pygame.font.Font(None, 32)
    color = pygame.Color('dodgerblue2')
    clock = pygame.time.Clock()
    is_running = True
    screen.fill((255, 0, 0))
    txt_surface = font.render("Не сдавайтесь, попробуйте ещё раз",
                              True, color)
    screen.blit(txt_surface, (50, 200))
    repeat_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((225, 575), (200, 50)),
                                                 text='Попробовать снова',
                                                 manager=manager)
    level_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((225, 627), (200, 50)),
                                                text='Выбрать уровень',
                                                manager=manager)

    while is_running:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == repeat_button:
                    main_screen(name_map)
                elif event.ui_element == level_button:
                    level(screen, clock)

            manager.process_events(event)

        manager.update(time_delta)
        manager.draw_ui(screen)

        pygame.display.update()
    pygame.quit()
