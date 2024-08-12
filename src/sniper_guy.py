import pygame

from enemy import Enemy
from bullet import Bullet
from world import World

from directions import *


class SniperGuy(Enemy):

    def __init__(self, position, size, speed, image, lives):
        super().__init__(position, size, speed, image, lives)

        self.take_damage = True
        self.bullets = pygame.sprite.Group()
        self.cooldown = 0

    def update(self):
        self.shoot()
        self.apply_gravity()
        self.move_and_check_collisions()
        self.apply_cooldown()
        self.check_boundaries()
        self.check_alive()

    def shoot(self):
        if self.cooldown <= 0:
            bullet = Bullet((self.rect.x, self.rect.y + (2 / 5) * self.rect.height), (24, 4), 32, LEFT)
            self.bullets.add(bullet)
            World.all_sprites.add(bullet)
            self.cooldown = 120

    def apply_cooldown(self):
        if self.cooldown > 0:
            self.cooldown -= 1
