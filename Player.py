import xml.etree.ElementTree as ET
import pytmx
import pygame
from pygame.sprite import Sprite

from settings import *


class Hero(Sprite):
    def __init__(self, screen, player_image_path, pos_x, pos_y, *group):
        super().__init__(*group)
        self.image = pygame.image.load(player_image_path)
        self.rect = self.image.get_rect().move(pos_x * tile_width, pos_y * tile_width)
        self.pos = [pos_x * tile_width, pos_y * tile_width]
        self.screen = screen

    def move(self, arrow, is_jump):
        t = LEN_JUMP - is_jump
        if arrow == "d":
            dx, dy = DIRECTIONS

            new_x = self.pos[0] + dx
            new_y = self.pos[1] - dy

            # if self.is_move_valid(new_x, new_y):
            self.pos[0] += dx
            self.pos[1] -= dy

            self.pos[0] += A_XY[0] * t
            self.pos[1] -= A_XY[1] * t

            self.rect = self.rect.move(self.pos[0], self.pos[1])

        if arrow == "a":
            dx, dy = DIRECTIONS

            new_x = self.pos[0] - dx
            new_y = self.pos[1] - dy
            # if self.is_move_valid(new_x, new_y):
            self.pos[0] -= dx
            self.pos[1] -= dy
            print(self.pos[0], self.pos[1])

            self.pos[0] -= A_XY[0] * t
            self.pos[1] -= A_XY[1] * t

            self.rect = self.rect.move(self.pos[0], self.pos[1])



