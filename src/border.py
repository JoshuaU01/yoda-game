import pygame

from object import Object

from colors import *

class Border(Object):
    def __init__(self, width, height, x, y):
        super().__init__()
        self.image = pygame.Surface([width, height], pygame.SRCALPHA)
        #self.image.fill(RED)  # Debug purposes
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)