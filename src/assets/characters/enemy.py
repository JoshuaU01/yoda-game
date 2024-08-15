import pygame

from src.assets.character import Character
from src.environment.world import World


class Enemy(Character):
    """
    A super class for all enemy types.
    """

    def __init__(
            self, position: tuple[int, int], size: tuple[int, int], speed: int, image: pygame.Surface,
            lives: int) -> None:
        """
        Creates an instance of this class.

        Args:
            position (tuple[int, int]): The position of the top left corner of the enemy.
            size (tuple[int, int]): The size of the enemy.
            speed (int): The maximum speed of the enemy.
            image (pygame.Surface): The image of the enemy.
            lives (int): The number of lives of the enemy.
        """
        super().__init__(position, size, speed, image, lives)
        self.gravity = 1.3
        self.on_ground = False
        self.take_damage = True

    def update(self) -> None:
        """
        Updates the enemy with every frame.
        """
        self.apply_gravity()
        self.update_position_x()
        self.update_position_y()
        self.check_boundaries()
        self.check_alive()

    def apply_gravity(self) -> None:
        """
        Pulls the enemy down while in the air.
        """
        if not self.on_ground:
            self.velocity.y += self.gravity
