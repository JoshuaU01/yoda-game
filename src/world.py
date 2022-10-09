import pygame

class World:

    def __init__(self, background, size, blocks, enemies, gravity=9.81):
        self.gravity = gravity
        self.size = size
        self.background = pygame.image.load(background)
        self.background = pygame.transform.scale(self.background, self.size)
        self.blocks = blocks
        self.enemies = enemies