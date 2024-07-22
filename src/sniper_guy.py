import pygame

from enemy import Enemy

class SniperGuy(Enemy):

    def __init__(self, position, size, speed, image, lives):
        super().__init__(position, size, speed, image, lives)

    def shoot(self):
        pass