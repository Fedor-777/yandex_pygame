import pygame
import pygame_gui


def victory(screen, clock):
    manager = pygame_gui.UIManager((800, 600))
    time_delta = clock.tick(60) / 1000.0
    clock = pygame.time.Clock()
    is_running = True
    screen.fill((0, 255, 0))

    win = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((225, 550), (175, 50)),
                                                text='Следующий уровень',
                                                manager=manager)

    while is_running:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == win:
                    return True

            manager.process_events(event)

        manager.update(time_delta)
        manager.draw_ui(screen)

        pygame.display.update()
    return False


screen = pygame.display.set_mode((600, 1200))
clock = pygame.time.Clock()
victory(screen, clock)