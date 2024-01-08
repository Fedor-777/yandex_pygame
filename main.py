import os

import pygame
from login import login
from main_screen import main_screen


player_name = login()

main_screen()

pygame.quit()