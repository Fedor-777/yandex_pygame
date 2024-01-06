import sys

import pygame
from pygame.sprite import Sprite


from settings import *
from functoins import load_image

class Hero(Sprite):
    def __init__(self, screen, player_image_path, *group):
        super().__init__(*group)
        self.image = pygame.image.load(player_image_path)
        self.rect = self.image.get_rect()
        self.rect.move_ip(200, 500)
        self.screen = screen

    def move(self, arrow, is_jump, wall_group):
        t = LEN_JUMP - is_jump
        dx, dy = DIRECTIONS
        temp_sprite = Hero(self.screen, HERO_IMAGE)
        temp_sprite.rect = self.rect.copy()

        if arrow == "d":
            point = 1
        if arrow == "a":
            point = -1

        temp_sprite.rect.move_ip(dx * point - A_XY[0] * t, -dy - A_XY[1] * t)
        collisions = pygame.sprite.spritecollide(temp_sprite, wall_group, False)
        if not collisions:
            self.rect.move_ip(dx * point - A_XY[0] * t, -dy - A_XY[1] * t)
            return is_jump
        else:
            print([self.rect.x, self.rect.y], [collisions[0].rect.x, collisions[0].rect.y])
            if self.rect.x < collisions[0].rect.x:
                self.rect.move_ip(collisions[0].rect.x - self.rect.x - tile_width, 0)
            elif self.rect.x >= collisions[0].rect.x:
                self.rect.move_ip(collisions[0].rect.x - self.rect.x + tile_width, 0)
            return 0

class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__()
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


"""pygame.init()
clock = pygame.time.Clock()
# Определяем размеры экрана
screen_width = 300
screen_height = 300

# Создаем окно
screen = pygame.display.set_mode((screen_width, screen_height))

sheet = load_image("тыква смерть.png")

# Создаем экземпляр класса AnimatedSprite
animated_sprite = AnimatedSprite(sheet, 6, 1, 100, 100)

# Создаем группу спрайтов
all_sprites = pygame.sprite.Group()
all_sprites.add(animated_sprite)

# Главный цикл игры
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Обновляем спрайты
    all_sprites.update()

    # Отрисовываем спрайты на экране
    screen.fill((0, 0, 0))  # Заливаем экран черным цветом
    all_sprites.draw(screen)
    clock.tick(7)
    pygame.display.flip()

# Завершаем работу pygame и выходим из программы
pygame.quit()
sys.exit()"""
