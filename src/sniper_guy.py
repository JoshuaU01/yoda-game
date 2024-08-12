from typing import Tuple

import pygame

from enemy import Enemy
from bullet import Bullet
from world import World

from directions import *


class SniperGuy(Enemy):
    """
    A long-range combat enemy type that can run towards the player.
    """

    def __init__(
            self, position: Tuple[int, int], size: Tuple[int, int], speed: int, image: pygame.Surface,
            lives: int) -> None:
        """
        Creates an instance of this class.

        Args:
            position (Tuple[int, int]): The position of the top left corner of the sniper guy.
            size (Tuple[int, int]): The size of the sniper guy.
            speed (int): The maximum speed of the sniper guy.
            image (pygame.Surface): The image of the sniper guy.
            lives (int): The number of lives of the sniper guy.
        """
        super().__init__(position, size, speed, image, lives)

        self.take_damage = True
        self.bullets = pygame.sprite.Group()
        self.cooldown = 0

    def update(self) -> None:
        """
        Updates the sniper guy enemy with every frame.
        """
        self.shoot()
        self.apply_gravity()
        self.move_and_check_collisions()
        self.apply_cooldown()
        self.check_boundaries()
        self.check_alive()

    def shoot(self) -> None:
        """
        Lets the sniper guy shoot bullets.
        """
        if self.cooldown <= 0:
            bullet = Bullet((self.rect.x, self.rect.y + (2 / 5) * self.rect.height), (24, 4), 32, LEFT)
            self.bullets.add(bullet)
            World.all_sprites.add(bullet)
            self.cooldown = 120

    def apply_cooldown(self) -> None:
        """
        Counts down a timer for the next allowed shot.
        """
        if self.cooldown > 0:
            self.cooldown -= 1
