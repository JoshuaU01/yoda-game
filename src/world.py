import pygame

class World:

    def __init__(self, background, size, blocks, enemies, gravity=9.81):
        self.gravity = gravity
        self.size = size
        self.background = background
        self.blocks = blocks
        self.enemies = enemies
        self.hitbox = pygame.Rect(-100, 686, 1640, 200)
        self.take_damage = False

    def draw(self, screen, show_hitbox=False):
        screen.blit(self.background, (0, 0))
        if show_hitbox:
            pygame.draw.rect(screen, (255,0,0), self.hitbox, 5)