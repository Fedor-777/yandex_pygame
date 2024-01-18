import os
import sqlite3
import sys

import pygame
import pytmx


def load_map(tmx_file):
    tmx_data = pytmx.load_pygame(tmx_file)

    map_width = tmx_data.width
    map_height = tmx_data.height

    # Создаем двумерную таблицу для хранения данных карты
    map_array = [[0 for _ in range(map_width)] for _ in range(map_height)]

    # Заполняем двумерную таблицу данными из TMX-файла
    for layer in tmx_data.layers:
        if layer.name == 'Слой тайлов 1':
            for x, y, gid in layer:
                map_array[y][x] = gid
    return map_array


def load_image(name, colorkey=None, size=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    # Можно сразу удалить задний фон
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    # Можно сразу сжать картинку до нужного размера
    if size is not None:
        image = pygame.transform.scale(image, size)
    return image


def calculate_rating(nick_player):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT lvl1, lvl2, lvl3, lvl4, lvl5, lvl6, money1, money2, money3, money4, money5, money6 FROM stats WHERE nick_player = ?",
            (nick_player,))
        data = cursor.fetchone()

        if data:
            weights = [15, 15, 20, 25, 25, 25]
            total_rating = sum(
                max(0, 100 - time) * weight if time > 0 else 0 for time, weight in zip(data[:6], weights))
            total_coins = sum(data[6:])
            return total_rating, total_coins
        else:
            return None, None
    except sqlite3.Error as e:
        return None, None
    finally:
        conn.close()
