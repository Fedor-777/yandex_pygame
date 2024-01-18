from pygame.sprite import Sprite

from settings import tile_width, tile_height


class Tile(Sprite):
    def __init__(self, my_map, pos_x, pos_y, key=False, *group):
        super().__init__(*group)
        if key:
            self.image = my_map.get_tile_image(1, 1, 0)
            self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        else:
            self.image = my_map.get_tile_image(pos_x, pos_y, 0)
            self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)