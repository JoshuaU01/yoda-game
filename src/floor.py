import pygame

from colors import *

class Floor(pygame.sprite.Sprite):
    def __init__(self, width, height, x, y, image):
        super().__init__()
        self.image = pygame.Surface([width, height], pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)