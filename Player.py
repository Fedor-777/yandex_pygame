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
            new_x = self.pos[0] + dx
            new_y = self.pos[1] - dy
            if 0 <= new_x <= WINDOW_WIGHT // tile_width and 0 <= new_y <= WINDOW_HEIGHT // tile_width:
                self.pos[0] += dx
                self.pos[1] -= dy
                self.pos[0] -= A_XY[0] * t
                self.pos[1] -= A_XY[1] * t
                print(self.pos[0], self.pos[1])

        if arrow == "a":
            new_x = self.pos[0] - dx
            new_y = self.pos[1] - dy
            if 0 < new_x < WINDOW_WIGHT // tile_width and 0 < new_y < WINDOW_HEIGHT // tile_width:
                self.pos[0] -= dx
                self.pos[1] -= dy
                self.pos[0] -= A_XY[0] * t
                self.pos[1] -= A_XY[1] * t
                if self.pos[1] > WINDOW_HEIGHT // tile_width:
                    self.pos[1] = WINDOW_HEIGHT // tile_width
                if self.pos[1] < 0:
                    self.pos[1] = 0
                if self.pos[0] < 0:
                    self.pos[0] = 0
                if self.pos[0] > WINDOW_WIGHT // tile_width:
                    self.pos[0] = WINDOW_WIGHT // tile_width
                print(self.pos[0], self.pos[1])

        self.rect = self.image.get_rect().move(self.pos[0] * tile_width, self.pos[1] * tile_height)
