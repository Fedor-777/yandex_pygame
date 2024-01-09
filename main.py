from login import login
from screens import *

player_name = login()
screen = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()

level(screen, clock, player_name)

pygame.quit()
