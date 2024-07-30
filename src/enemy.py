import pygame

from character import Character

from colors import *

class Enemy(Character):

    def __init__(self, position, size, speed, image, lives):
        super().__init__(position, size, speed, image, lives)
        self.take_damage = True

    def update(self):
        self.check_alive()