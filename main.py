# import libraries
import pygame
import random
import os

from spritesheet import SpriteSheet
from global_variables import *
from platform import Platform
from enemy import Enemy

# initialise pygame
pygame.init()

# create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Ducky')

# set frame rate
clock = pygame.time.Clock()
FPS = 35


if os.path.exists("score.txt"):
    with open("score.txt", 'r') as file:
        high_score = int(file.read())
else:
    high_score = 0


# load images
player_img = pygame.image.load('assets/duck.png').convert_alpha()
bg_image = pygame.image.load('assets/sky.png').convert_alpha()
platform_image = pygame.image.load('assets/platform_wood.png').convert_alpha()
platform_broken_image = pygame.image.load('assets/platform_broken.png').convert_alpha()
# bird sprite-sheet
bird_sheet_img = pygame.image.load('assets/bird.png').convert_alpha()
bird_sheet = SpriteSheet(bird_sheet_img)


# function for outputting text onto the screen
def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))


# function for drawing the background
def draw_bg(bg_scroll):
    screen.blit(bg_image, (0, 0 + bg_scroll))
    screen.blit(bg_image, (0, -600 + bg_scroll))


# function for drawing info panel
def draw_panel():
    pygame.draw.rect(screen, PANEL, (0, 0, SCREEN_WIDTH, 30))
    pygame.draw.line(screen, WHITE, (0, 30), (SCREEN_WIDTH, 30))
    draw_text(" SCORE: " + str(score // 100), font_small, WHITE, 0, 0)


# player class
class Player:
    def __init__(self, x, y):
        self.image = pygame.transform.scale(player_img, (50, 50))
        self.width = 25
        self.height = 40
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)
        self.vel_y = 0
        self.flip = False
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        # reset variables
        scroll = 0
        dx = 0
        dy = 0

        # process key presses
        key = pygame.key.get_pressed()

        if key[pygame.K_LEFT]:
            dx = -10
            self.flip = True
        if key[pygame.K_RIGHT]:
            dx = 10
            self.flip = False

        # gravity
        self.vel_y += GRAVITY
        dy += self.vel_y

        # ensure player teleports if it goes of the edge off the screen
        if self.rect.left + dx < 0:
            # dx = - self.rect.left
            dx = SCREEN_WIDTH - self.rect.right
        if self.rect.right + dx > SCREEN_WIDTH:
            dx = -self.rect.left

        # check collision with platforms
        for platform in platform_group:
            # collision in y direction
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                # check if above the platform
                if self.rect.bottom < platform.rect.centery:
                    if self.vel_y > 0:
                        self.rect.bottom = platform.rect.top
                        dy = 0
                        self.vel_y = -20
                        # destroy platform if it is broken
                        platform.destroy()


        # check if the player has bounced to the top of the screen
        if self.rect.top <= SCROLL_THRESH:
            # if player is jumping
            if self.vel_y < 0:
                scroll = -dy

        # update rectangle position
        self.rect.x += dx
        self.rect.y += dy + scroll



        return scroll

    def draw(self):
        # flip the image (False is for up or down)
        screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x - 11, self.rect.y - 3))
        # pygame.draw.rect(screen, WHITE, self.rect, 2)


# player instance
ducky = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)

# create sprite groups
platform_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

# create starting platform
platform = Platform(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 20, 100, False, False, platform_image)
platform_group.add(platform)


# game loop
run = True
while run:

    clock.tick(FPS)

    if game_over is False:
        scroll = ducky.move()

        # draw background
        bg_scroll += scroll
        if bg_scroll >= 600:
            bg_scroll = 0
        draw_bg(bg_scroll)

        # generate platforms
        if len(platform_group) < MAX_PLATFORMS:
            p_w = random.randint(60, 70)
            p_x = random.randint(0, SCREEN_WIDTH - p_w)
            p_y = platform.rect.y - random.randint(80, 100)
            # 1 - normal | 2 - moving | 3 - broken | 4 - broken - moving
            p_type = random.choice([1]*6 + [2]*3 + [3]*3 + [4]*3)
            if p_type == 2 and score > 400 or p_type == 4 and score > 2000:
                p_moving = True
            else:
                p_moving = False
            if p_type == 3 and score > 100 or p_type == 4 and score > 2000:
                p_broken = True
            else:
                p_broken = False
            if p_broken is True:
                platform = Platform(p_x, p_y, p_w, p_broken, p_moving, platform_broken_image)
            else:
                platform = Platform(p_x, p_y, p_w, p_broken, p_moving, platform_image)
            platform_group.add(platform)

        # update platforms
        platform_group.update(scroll)

        # generate enemies
        if len(enemy_group) == 0 and score > 3000:
            enemy = Enemy(SCREEN_WIDTH, 100, bird_sheet, 1.5)
            enemy_group.add(enemy)

        # update enemies
        enemy_group.update(scroll, SCREEN_WIDTH)

        # update score
        if scroll > 0:
            score += scroll

        # draw line at previous high score
        pygame.draw.line(screen, WHITE, (0, score - high_score + SCREEN_HEIGHT - SCROLL_THRESH), (SCREEN_WIDTH, score - high_score + SCREEN_HEIGHT - SCROLL_THRESH), 3)
        draw_text("HIGH SCORE", font_small, WHITE, SCREEN_WIDTH - 130, score - high_score + SCREEN_HEIGHT - SCROLL_THRESH)
        # draw sprites
        platform_group.draw(screen)
        enemy_group.draw(screen)
        ducky.draw()

        # draw panel
        draw_panel()

        # check game over
        if ducky.rect.top > SCREEN_HEIGHT:
            game_over = True
        # check for collision with enemies
        if pygame.sprite.spritecollide(ducky, enemy_group, False):
            if pygame.sprite.spritecollide(ducky, enemy_group, False, pygame.sprite.collide_mask):
                game_over = True

    else:
        if fade_counter < SCREEN_WIDTH:
            pass
            fade_counter += 5
            for y in range(0, 6, 2):
                pygame.draw.rect(screen, BLACK, (0, y * 100, fade_counter, SCREEN_HEIGHT / 6))
                pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH - fade_counter, (y + 1) * 100, SCREEN_WIDTH, SCREEN_HEIGHT / 6))
        else:
            draw_text("GAME OVER!", font_big, WHITE, 130, 200)
            draw_text("SCORE: " + str(score // 100), font_big, WHITE, 150, 250)
            draw_text("PRESS SPACE TO PLAY AGAIN", font_big, WHITE, 25, 300)
            key = pygame.key.get_pressed()

            # update high score
            if score > high_score:
                high_score = score
                with open("score.txt", 'w') as file:
                    file.write(str(high_score))

            # restart game
            if key[pygame.K_SPACE]:
                # reset variables
                game_over = False
                score = 0
                scroll = 0
                fade_counter = 0
                # reposition Ducky
                ducky.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)
                # reset enemies
                enemy_group.empty()
                # reset platforms
                platform_group.empty()
                # create starting platform
                platform = Platform(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 20, 100, False, False, platform_image)
                platform_group.add(platform)

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # update high score
            if score > high_score:
                high_score = score
                with open("score.txt", 'w') as file:
                    file.write(str(high_score))
            run = False

    # update display window
    pygame.display.update()


pygame.quit()
