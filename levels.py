import pygame
import pygame_gui
from settings import *


def level(screen, clock):
    manager = pygame_gui.UIManager((800, 600))
    is_running = True
    screen.fill((0, 255, 0))

    first_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((150, 200), (50, 50)),
                                                text='1',
                                                manager=manager)
    second_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((200, 200), (50, 50)),
                                                text='2',
                                                manager=manager)
    third_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 200), (50, 50)),
                                                text='3',
                                                manager=manager)
    fourth_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((150, 255), (50, 50)),
                                                text='4',
                                                manager=manager)
    fifth_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((200, 255), (50, 50)),
                                                text='5',
                                                manager=manager)
    sixth_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 255), (50, 50)),
                                                text='6',
                                                manager=manager)

    while is_running:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == first_button:
                    return True

            manager.process_events(event)

        manager.update(time_delta)
        manager.draw_ui(screen)

        pygame.display.update()
    return False

pygame.init()
screen = pygame.display.set_mode((400, 500))
clock = pygame.time.Clock()
level(screen, clock)