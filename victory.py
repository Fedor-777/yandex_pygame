import pygame


class Victory:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font(None, 25)

        self.button_x = screen_width // 2 - 100
        self.button_y = screen_height // 2 + 50
        self.button_width = 200
        self.button_height = 50

    def display(self, screen):
        victory_bg_color = (0, 255, 0)
        screen.fill(victory_bg_color)

        text = self.font.render("Поздравляем! Вы победили!", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        screen.blit(text, text_rect)

        # кнопка
        button_rect = pygame.Rect(self.button_x, self.button_y, self.button_width, self.button_height)
        pygame.draw.rect(screen, (0, 0, 255), button_rect)
        button_text = self.font.render("Следующий уровень", True, (255, 255, 255))
        button_text_rect = button_text.get_rect(center=button_rect.center)
        screen.blit(button_text, button_text_rect)

        pygame.display.flip()

    def check_button_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = event.pos
                if self.button_x <= mouse_x <= self.button_x + self.button_width \
                        and self.button_y <= mouse_y <= self.button_y + self.button_height:
                    return True
        return False
