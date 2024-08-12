from typing import Tuple

import pygame

from character import Character
from world import World

from colors import *


class Enemy(Character):
    """
    A super class for all enemy types.
    """

    def __init__(
            self, position: Tuple[int, int], size: Tuple[int, int], speed: int, image: pygame.Surface,
            lives: int) -> None:
        """
        Creates an instance of this class.

        Args:
            position (Tuple[int, int]): The position of the top left corner of the enemy.
            size (Tuple[int, int]): The size of the enemy.
            speed (int): The maximum speed of the enemy.
            image (pygame.Surface): The image of the enemy.
            lives (int): The number of lives of the enemy.
        """
        super().__init__(position, size, speed, image, lives)
        self.gravity = 1.4
        self.on_ground = False
        self.take_damage = True

    def update(self) -> None:
        """
        Updates the enemy with every frame.
        """
        self.apply_gravity()
        self.move_and_check_collisions()
        self.check_boundaries()
        self.check_alive()

    def apply_gravity(self) -> None:
        """
        Pulls the enemy down while in the air.
        """
        if not self.on_ground:
            self.velocity.y += self.gravity

    def move_and_check_collisions(self) -> None:
        """
        Calculates the new position of the enemy with respect to their movement and other assets.
        """
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
