import pygame

from character import Character
from world import World

from colors import *

class Enemy(Character):

    def __init__(self, position, size, speed, image, lives):
        super().__init__(position, size, speed, image, lives)
        self.gravity = 1.4
        self.on_ground = False
        self.take_damage = True

    def update(self):
        self.check_alive()
        self.apply_gravity()
        self.move_and_check_collisions()

    def apply_gravity(self):
        if not self.on_ground:
            self.velocity.y += self.gravity

    def move_and_check_collisions(self):
        old_rect = self.rect.copy()

        # Check for collision in horizontal direction
        self.rect.x += self.velocity.x
        if pygame.sprite.spritecollideany(self, World.blocks):
            self.rect.x = old_rect.x

        # Check for collision in vertical direction
        self.rect.y += self.velocity.y
        collision_block = pygame.sprite.spritecollideany(self, World.blocks)
        if collision_block:
            if self.velocity.y > 0:
                self.rect.bottom = collision_block.rect.top
                self.velocity.y = 0
                self.on_ground = True
            elif self.velocity.y < 0:
                self.rect.top = collision_block.rect.bottom
                self.velocity.y = 0
        else:
            self.on_ground = False