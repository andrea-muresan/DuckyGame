import pygame
import random

from global_variables import *


# the platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, broken, moving, platform_image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(platform_image, (width, 10))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.broken = broken
        self.moving = moving
        self.move_counter = random.randint(0, 50)
        self.direction = random.choice([-1, 1])
        self.speed = random.randint(1, 2)

    def update(self, scroll):
        # moving platform side to side if it is a moving platform
        if self.moving is True:
            self.move_counter += 1
            self.rect.x += self.direction * self.speed

        # change platform direction if it has moved fully or hit a wall
        if self.move_counter >= 100 or self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.direction *= -1
            self.move_counter = 0

        # update platforms vertical position
        self.rect.y += scroll

        # check if the platform has gone under the screen
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

    def destroy(self):
        # destroy a broken platform
        if self.broken is True:
            self.kill()
