import os
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
    print(map_array)
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
