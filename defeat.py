import pygame
import pygame_gui


def defeat(screen, clock):
    manager = pygame_gui.UIManager((800, 600))
    time_delta = clock.tick(60) / 1000.0
    clock = pygame.time.Clock()
    is_running = True
    screen.fill((255, 0, 0))

    hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 575), (100, 50)),
                                                text='Попробовать снова',
                                                manager=manager)

    while is_running:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == hello_button:
                    return True

            manager.process_events(event)

        manager.update(time_delta)
        manager.draw_ui(screen)

        pygame.display.update()
    return False