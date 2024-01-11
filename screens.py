import os
import sqlite3
import time

import pygame
import pygame_gui
import pytmx

from Player import Hero
from Tile import Tile
from functoins import load_map, calculate_rating
from settings import *

volume = 0.5


def main_screen(player_name, name_map):
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
    map = pytmx.load_pygame(full_tmx_path)
    map_array = load_map(full_tmx_path)
    height = map.height
    width = map.width
    # music
    current_dir = os.path.dirname(__file__)
    sound_file_path_vic = os.path.join(current_dir, "sounds", "game-won.wav")
    sound_file_path_lose = os.path.join(current_dir, "sounds", "lose.wav")

    vic = pygame.mixer.Sound(sound_file_path_vic)
    vic.set_volume(1)
    los = pygame.mixer.Sound(sound_file_path_lose)
    los.set_volume(1)

    for y in range(height):
        for x in range(width):
            if x == 10 and y == 49:
                Tile(map, x, y, background_group)
                new_player = Hero(screen, player_group)
            elif map_array[y][x] == 1 or map_array[y][x] == 3 or map_array[y][x] == 4 or map_array[y][x] == 6 or \
                    map_array[y][x] == 8 or map_array[y][x] == 10 or map_array[y][x] == 11:
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
                    victory(screen, elapsed_time, int(name_map[-5]), player_name)
                    is_jump = 0
                    running = False

        finish_collisions = pygame.sprite.spritecollide(new_player, finish_group, False)
        defeat_collisions = pygame.sprite.spritecollide(new_player, obstacles_group, False)

        if finish_collisions:
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(elapsed_time)
            vic.play()
            victory(screen, elapsed_time, int(name_map[-5]), player_name)
            is_jump = 0
            running = False
        elif defeat_collisions:
            los.play()
            defeat(screen, clock, name_map, player_name)
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


def level(screen, clock, player_name):
    global volume
    manager = pygame_gui.UIManager(WINDOW_SIZE)
    is_running = True
    screen = pygame.display.set_mode((500, 600))
    screen.fill((0, 0, 255))
    font = pygame.font.SysFont(None, 35)
    text = "Громкость:"
    text_surf = font.render(text, True, (255, 0, 0))
    screen.blit(text_surf, (42, 50))
    first_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 200), (100, 100)),
                                                text='1',
                                                manager=manager)
    second_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((152, 200), (100, 100)),
                                                 text='2',
                                                 manager=manager)
    third_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((254, 200), (100, 100)),
                                                text='3',
                                                manager=manager)
    fourth_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 302), (100, 100)),
                                                 text='4',
                                                 manager=manager)
    fifth_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((152, 302), (100, 100)),
                                                text='5',
                                                manager=manager)
    sixth_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((254, 302), (100, 100)),
                                                text='6',
                                                manager=manager)
    # volume
    volume_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((180, 50), (200, 30)),
                                                           start_value=volume,
                                                           value_range=(0.0, 1.0),
                                                           manager=manager)
    stats_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 404), (304, 50)),
                                                text='рейтинг',
                                                manager=manager)

    while is_running:
        time_delta = clock.tick(60) / 1000.0
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                is_running = False

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == first_button:
                    main_screen(player_name, "уровень1.tmx")
                elif event.ui_element == second_button:
                    main_screen(player_name, "уровень2.tmx")
                elif event.ui_element == third_button:
                    main_screen(player_name, "уровень3.tmx")
                elif event.ui_element == fourth_button:
                    main_screen(player_name, "уровень4.tmx")
                elif event.ui_element == fifth_button:
                    main_screen(player_name, "уровень5.tmx")
                elif event.ui_element == sixth_button:
                    main_screen(player_name, "уровень6.tmx")
                elif event.ui_element == stats_button:
                    leader_board(screen, clock, player_name)

            manager.process_events(event)

        manager.update(time_delta)
        manager.draw_ui(screen)

        volume = volume_slider.get_current_value()
        pygame.mixer.music.set_volume(volume)
        pygame.display.update()

    pygame.quit()


def victory(screen, elapsed_time, number_of_lvl, player_name):
    manager = pygame_gui.UIManager(WINDOW_SIZE)
    font = pygame.font.Font(None, 32)
    color = pygame.Color('darkmagenta')
    clock = pygame.time.Clock()
    is_running = True

    screen.fill((0, 255, 0))
    elapsed_time = int(elapsed_time)
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    if number_of_lvl == 1:
        cursor.execute('UPDATE stats SET lvl1 = ? WHERE nick_player = ?', (elapsed_time, player_name))
    elif number_of_lvl == 2:
        cursor.execute('UPDATE stats SET lvl2 = ? WHERE nick_player = ?', (elapsed_time, player_name))
    elif number_of_lvl == 3:
        cursor.execute('UPDATE stats SET lvl3 = ? WHERE nick_player = ?', (elapsed_time, player_name))
    elif number_of_lvl == 4:
        cursor.execute('UPDATE stats SET lvl4 = ? WHERE nick_player = ?', (elapsed_time, player_name))
    elif number_of_lvl == 5:
        cursor.execute('UPDATE stats SET lvl5 = ? WHERE nick_player = ?', (elapsed_time, player_name))
    elif number_of_lvl == 6:
        cursor.execute('UPDATE stats SET lvl6 = ? WHERE nick_player = ?', (elapsed_time, player_name))

    connection.commit()
    connection.close()
    if elapsed_time == 2 or elapsed_time == 3 or elapsed_time == 4:
        txt_surface = font.render("Поздравляем, вы прошли уровень " + f"{number_of_lvl} за {elapsed_time} секунды",
                                  True, color)
    else:
        txt_surface = font.render("Поздравляем, вы прошли уровень " + f"{number_of_lvl} за {elapsed_time} секунд",
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
                    level(screen, clock, player_name)

            manager.process_events(event)

        manager.update(time_delta)
        manager.draw_ui(screen)

        pygame.display.update()
    pygame.quit()


def defeat(screen, clock, name_map, player_name):
    manager = pygame_gui.UIManager((800, 1000))
    font = pygame.font.Font(None, 32)
    color = pygame.Color('lawngreen')
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
                    main_screen(player_name, name_map)
                elif event.ui_element == level_button:
                    level(screen, clock, player_name)

            manager.process_events(event)

        manager.update(time_delta)
        manager.draw_ui(screen)

        pygame.display.update()
    pygame.quit()


def leader_board(screen, clock1, player_name):
    pygame.init()
    manager = pygame_gui.UIManager((500, 600))
    clock = pygame.time.Clock()
    is_running = True
    screen.fill((29, 102, 110))
    return_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((150, 510), (200, 50)),
                                                 text='Вернуться назад',
                                                 manager=manager)
    while is_running:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == return_button:
                    level(screen, clock1, player_name)

            manager.process_events(event)

        i = 35
        column_space = 200
        font_style = pygame.font.Font(None, 32)
        color = pygame.Color('darkorange3')
        rating = font_style.render(f'ТОП ЛУЧШИХ ИГРОКОВ', True, color)
        head1 = font_style.render(f'МЕСТО', True, color)
        head2 = font_style.render(f'ИГРОК', True, color)
        head3 = font_style.render(f'СЧЁТ', True, color)
        dis_width = 50

        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute('SELECT nick_player FROM stats')
        nicks = cursor.fetchall()
        for nick in nicks:
            nick = nick[0]
            score = calculate_rating(nick)
            cursor.execute('UPDATE stats SET score = ? WHERE nick_player = ?', (score, nick))

        screen.blit(rating, [120, 40])
        screen.blit(head1, [dis_width / 5, (300 / 4) + 5])
        screen.blit(head2, [dis_width / 5 + column_space, (300 / 4) + 5])
        screen.blit(head3, [dis_width / 5 + column_space * 2, (300 / 4) + 5])

        cursor.execute('SELECT * FROM stats ORDER BY score DESC LIMIT 10')
        rows = cursor.fetchall()
        for index, row in enumerate(rows):
            place = index + 1
            player = row[1]
            player_score = row[2]

            if player == player_name:
                text_player_place = font_style.render(f'{place}', True, pygame.Color('firebrick4'))
                text_player_name = font_style.render(f'{player}', True, pygame.Color('firebrick4'))
                text_player_score = font_style.render(f'{player_score}', True, pygame.Color('firebrick4'))
            else:
                text_player_place = font_style.render(f'{place}', True, color)
                text_player_name = font_style.render(f'{player}', True, color)
                text_player_score = font_style.render(f'{player_score}', True, color)

            screen.blit(text_player_place, [dis_width / 5, (300 / 4) + i + 5])
            screen.blit(text_player_name, [dis_width / 5 + column_space, (300 / 4) + i + 5])
            screen.blit(text_player_score, [dis_width / 5 + column_space * 2, (300 / 4) + i + 5])

            i += 35
        connection.commit()
        connection.close()

        pygame.display.flip()
        manager.update(time_delta)
        manager.draw_ui(screen)
    pygame.quit()
