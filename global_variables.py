import pygame

from spritesheet import SpriteSheet

pygame.init()

# game window
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# game variables
SCROLL_THRESH = 300
GRAVITY = 1
MAX_PLATFORMS = 10
scroll = 0
bg_scroll = 0
game_over = False
score = 0
fade_counter = 0

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PANEL = (153, 217, 234)

# define font
font_small = pygame.font.SysFont('Lucida Sans', 20)
font_big = pygame.font.SysFont('Lucida Sans', 25)
