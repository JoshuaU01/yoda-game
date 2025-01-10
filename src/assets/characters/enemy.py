from abc import ABC, abstractmethod

import pygame

from src.assets.character import Character
from src.environment.world import World, Directions


class Enemy(Character, ABC):
    """
    A super class for all enemy types.
    """

    @abstractmethod
    def __init__(
            self,
            position: tuple[int, int],
            size: tuple[int, int],
            speed: int,
            image: pygame.Surface,
            direction: Directions,
            health: int,
            can_take_damage: bool = True) \
            -> None:
        """
        Creates an instance of this class.

        Args:
            position (tuple[int, int]): The position of the top left corner of the enemy.
            size (tuple[int, int]): The size of the enemy.
            speed (int): The maximum speed of the enemy.
            image (pygame.Surface): The image of the enemy.
            direction (Directions): The initial horizontal direction the enemy is facing.
            health (int): The number of lives of the enemy.
            can_take_damage (bool): Whether the enemy can take damage.
        """
        sprite_groups = [World.all_sprites, World.enemies]
        super().__init__(
            position, size, speed, image, direction, health=health, can_take_damage=can_take_damage,
            sprite_groups=sprite_groups)
