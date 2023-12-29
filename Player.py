import pygame
from pygame.sprite import Sprite

from settings import *


class Hero(Sprite):
    def __init__(self, screen, player_image_path, pos_x, pos_y, *group):
        super().__init__(*group)
        self.image = pygame.image.load(player_image_path)
        self.rect = self.image.get_rect()
        self.rect.move_ip(200, 500)
        self.pos = [pos_x, pos_y]
        self.screen = screen

    def move(self, arrow, is_jump):
        t = LEN_JUMP - is_jump
        dx, dy = DIRECTIONS
        if arrow == "d":
            self.pos[0] += dx
            self.pos[1] -= dy
        if arrow == "a":
            self.pos[0] -= dx
            self.pos[1] -= dy

        self.rect = self.image.get_rect().move(self.pos[0] * tile_width, self.pos[1] * tile_height)
        self.pos[0] -= A_XY[0] * t
        self.pos[1] -= A_XY[1] * t
