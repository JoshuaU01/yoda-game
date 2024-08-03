import pygame

from enemy import Enemy
from bullet import Bullet
from world import World

from directions import *

class Runner(Enemy):

    def __init__(self, position, size, speed, image, lives):
        super().__init__(position, size, speed, image, lives)

        self.take_damage = True

    def update(self):
        self.apply_gravity()
        self.move_and_check_collisions()
        self.check_boundaries()
        self.check_alive()