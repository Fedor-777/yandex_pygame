import xml.etree.ElementTree as ET

import pygame
from pygame.sprite import Sprite

from settings import *


class Hero(Sprite):
    def __init__(self, screen, player_image_path, pos_x, pos_y, map_file, *group):
        super().__init__(*group)
        self.image = pygame.image.load(player_image_path)
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.pos = [pos_x, pos_y]
        self.screen = screen
        self.map_data = self.load_map(map_file)

    def load_map(self, map_file):
        tree = ET.parse(map_file)
        root = tree.getroot()
        map_data = []
        for layer in root.findall('layer'):
            data = layer.find('data').text.strip().split(',')
            map_data.append([int(tile.strip()) for tile in data])
        return map_data

    def move(self, arrow, is_jump):
        t = LEN_JUMP - is_jump
        if arrow == "d":
            dx, dy = DIRECTIONS

            new_x = self.pos[0] + dx
            new_y = self.pos[1] - dy
            if self.is_move_valid(new_x, new_y):
                self.pos[0] += dx
                self.pos[1] -= dy

                self.pos[0] += A_XY[0] * t
                self.pos[1] -= A_XY[1] * t

                self.rect = self.image.get_rect().move(self.pos[0], self.pos[1])
                print(self.pos)
        if arrow == "a":
            dx, dy = DIRECTIONS

            new_x = self.pos[0] - dx
            new_y = self.pos[1] - dy
            if self.is_move_valid(new_x, new_y):
                self.pos[0] -= dx
                self.pos[1] -= dy

                self.pos[0] -= A_XY[0] * t
                self.pos[1] -= A_XY[1] * t

                self.rect = self.image.get_rect().move(self.pos[0], self.pos[1])
                print(self.pos)



    # x // 20 >= len(self.map_data[0]) or y // 20 >= len(self.map_data)
    # self.map_data[y // 20][x // 20] == 23
    def is_move_valid(self, x, y):
        if x + tile_width < 0 or y + tile_width < 0 or x > WINDOW_WIGHT - tile_width or y > WINDOW_HEIGHT - tile_width:
            return False
        return True
