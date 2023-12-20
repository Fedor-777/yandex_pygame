import pygame

from settings import *


def login():
    pygame.init()
    window = pygame.display.set_mode(WINDOW_SIZE)
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, SIZE_TEXT)
    text = ""
    input_active = True
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN and input_active:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                elif event.key == pygame.K_TAB:
                    print("Добавляем ник в бд:", text)
                    run = False
                else:
                    text += event.unicode

        window.fill((0, 0, 0))
        text_surf = font.render("Введите свой ник и нажмите таб:", True, (255, 255, 255))
        window.blit(text_surf, (40, 300))
        text_surf_input = font.render(text, True, (255, 0, 0))
        window.blit(text_surf_input, text_surf_input.get_rect(center=window.get_rect().center))
        pygame.display.flip()
        clock.tick(60)


