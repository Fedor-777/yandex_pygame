import xml.etree.ElementTree as ET

import pygame
from pygame.sprite import Sprite

from settings import tile_width, tile_height


class Hero(Sprite):
    def __init__(self, player_image_path, pos_x, pos_y, map_file, *group):
        super().__init__(*group)
        self.image = pygame.image.load(player_image_path)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.pos = [pos_x, pos_y]
        self.map_data = self.load_map(map_file)

    def load_map(self, map_file):
        tree = ET.parse(map_file)
        root = tree.getroot()
        map_data = []
        for layer in root.findall('layer'):
            data = layer.find('data').text.strip().split(',')
            map_data.append([int(tile.strip()) for tile in data])
        return map_data

    def move(self, napr):
        new_x = self.pos[0]
        new_y = self.pos[1]
        if napr == "w":
            new_y -= 1
        elif napr == "a":
            new_x -= 1
        elif napr == "s":
            new_y += 1
        elif napr == "d":
            new_x += 1

        # if 0 <= new_x <= len()
        self.pos = [new_x, new_y]
        self.rect = self.image.get_rect().move(tile_width * new_x, tile_height * new_y)

    def is_move_valid(self, x, y):
        if x < 0 or y < 0 or x >= len(self.map_data[0]) or y >= len(self.map_data):
            return False
        return self.map_data[y][x] == 23
