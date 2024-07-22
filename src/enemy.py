import pygame

from character import Character

from colors import *

class Enemy(Character):

    def __init__(self, position, size, speed, image, lives):
        super().__init__(position, size, speed, image, lives)
        self.take_damage = True

    def update(self):
        self.check_alive()

    def lose_lives(self, amount):
        self.lives -= amount


    def draw(self, screen, show_hitbox=False):
        screen.blit(self.image, (self.position.x, self.position.y))
        if show_hitbox:
            pygame.draw.rect(screen, RED, self.rect, 5)