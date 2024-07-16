import pygame

from block import Block

from colors import *

class World(pygame.sprite.Sprite):

    def __init__(self, background, size, blocks, enemies, gravity=9.81):
        super().__init__()
        self.gravity = gravity
        self.size = size
        self.background = background
        self.blocks = blocks
        self.enemies = enemies
        self.hitbox = pygame.Rect(-100, 686, 1640, 200)
        self.take_damage = False

    #def load_map(self):
        #self.blocks = [Block((550, 350), (40, 40)), Block((590, 350), (40, 40)), Block((630, 350), (40, 40)), Block((800, 250), (40, 40)), Block((840, 250), (40, 40))] #TODO

    def draw(self, screen, show_hitbox=False):
        screen.blit(self.background, (0, 0))
        if show_hitbox:
            pygame.draw.rect(screen, RED, self.hitbox, 5)