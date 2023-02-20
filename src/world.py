import pygame

class World:

    def __init__(self, background, size, blocks, enemies, gravity=9.81):
        self.gravity = gravity
        self.size = size
        self.background = background
        self.blocks = blocks
        self.enemies = enemies

    def draw(self, screen):
        screen.blit(self.background, (0, 0))