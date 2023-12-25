import os
import pygame
from pytmx import pytmx
from settings import *
from Player import Hero
from Tile import Tile


WINDOW_SIZE = WINDOW_WIGHT, WINDOW_HEIGHT = 400, 1000

class Level:
    def __init__(self, filename, free_tiles, finish, tiles_group, player_group, my_map, screen):
        self.screen = screen
        self.my_map = my_map
        self.player_group = player_group
        self.tiles_group = tiles_group
        tileset_filename = "Terrain (16x16).tsx"
        full_tmx_path = os.path.join("data", filename)
        full_tileset_path = os.path.join("data", tileset_filename)
        self.map = pytmx.load_pygame(full_tmx_path, tileset=full_tileset_path)
        self.height = self.map.height
        self.width = self.map.width
        self.tile_size = self.map.tilewidth
        self.free_tiles = free_tiles
        self.finish = finish



    def render(self):
        print(self.height, self.width)
        for y in range(self.height):
            for x in range(self.width):
                if x == 11 and y == 50:
                    new_player = Hero(self.screen, HERO_IMAGE, self.my_map, self.player_group)
                elif self.my_map[y][x] == 84:
                    Tile(self.my_map, x, y, self.tiles_group)
        return new_player
