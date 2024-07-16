import pygame

from character import Character

from colors import *

class Enemy(Character):

    def __init__(self, position, size, velocity, image):
        super().__init__(position, size, velocity, image)

        self.take_damage = True
        self.health = 5


    def die(self):
        if self.health <= 0:
            return True
        return False

    def draw(self, screen, show_hitbox=False):
        screen.blit(self.image, (self.position.x, self.position.y))
        if show_hitbox:
            pygame.draw.rect(screen, RED, self.rect, 5)