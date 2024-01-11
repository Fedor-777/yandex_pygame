from login import login
from screens import *

player_name = login()
volume = 0.5
screen = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()
pygame.mixer.music.load("sounds/music.mp3")
pygame.mixer.music.play(-1)

level(screen, clock, player_name)

pygame.quit()
