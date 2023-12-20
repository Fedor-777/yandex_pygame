import os
import pygame
import pytmx

WINDOW_SIZE = WINDOW_WIGHT, WINDOW_HEIGHT = 400, 1000

class Level:
    def __init__(self, filename, free_tiles, finish):
        tileset_filename = "Terrain (16x16).tsx"
        full_tmx_path = os.path.join("data", filename)
        full_tileset_path = os.path.join("data", tileset_filename)
        self.map = pytmx.load_pygame(full_tmx_path, tileset=full_tileset_path)
        self.height = self.map.height
        self.width = self.map.width
        self.tile_size = self.map.tilewidth
        self.free_tiles = free_tiles
        self.finish = finish

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                image = self.map.get_tile_image(x, y, 0)
                screen.blit(image, (x * self.tile_size, y * self.tile_size))

    def get_tile_id(self, pos):
        return self.map.tiledgidmap[self.map.get_tile_gid(*pos, 0)]

# pygame.init()
# screen = pygame.display.set_mode(WINDOW_SIZE)
# clock = pygame.time.Clock()
#
# level = Level("безымянный.tmx", [23], 117)
#
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#
#     screen.fill((0, 0, 0))
#     level.render(screen)
#     pygame.display.flip()
#     clock.tick(60)
#
# pygame.quit()
