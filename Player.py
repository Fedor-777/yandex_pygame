import pygame
from pygame.sprite import Sprite

from settings import *
from functoins import load_image


class Hero(Sprite):
    def __init__(self, screen, *group):
        super().__init__(*group)
        self.screen = screen
        self.frames = []
        sheet = load_image("тыква жизнь.png")
        self.cut_sheet(sheet, 5, 1)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect.move_ip(300, 1180)

    def move(self, arrow, is_jump, wall_group):
        t = LEN_JUMP - is_jump
        dx, dy = DIRECTIONS
        temp_sprite = Hero(self.screen)
        temp_sprite.rect = self.rect.copy()

        if arrow == "d":
            point = 1
        if arrow == "a":
            point = -1

        temp_sprite.rect.move_ip(dx * point - A_XY[0] * t, -dy - A_XY[1] * t)
        wall_collisions = pygame.sprite.spritecollide(temp_sprite, wall_group, False)

        if not wall_collisions:
            self.rect.move_ip(dx * point - A_XY[0] * t, -dy - A_XY[1] * t)
            return is_jump
        else:
            if self.rect.x < wall_collisions[0].rect.x:
                self.rect.move_ip(wall_collisions[0].rect.x - self.rect.x - tile_width, 0)
            elif self.rect.x >= wall_collisions[0].rect.x:
                self.rect.move_ip(wall_collisions[0].rect.x - self.rect.x + tile_width, 0)
            return 0

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
