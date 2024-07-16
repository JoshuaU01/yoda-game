import pygame

from enemy import Enemy

class SniperGuy(Enemy):

    def __init__(self, position, size, velocity, image):
        super().__init__(position, size, velocity, image)

    def shoot(self):
        pass