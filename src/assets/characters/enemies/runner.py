import pygame

from src.assets.characters.enemy import Enemy


class Runner(Enemy):
    """
    A melee enemy type that can run towards the player.
    """

    def __init__(
            self, position: tuple[int, int], size: tuple[int, int], speed: int, image: pygame.Surface,
            lives: int) -> None:
        """
        Creates an instance of this class.

        Args:
            position (tuple[int, int]): The position of the top left corner of the runner.
            size (tuple[int, int]): The size of the runner.
            speed (int): The maximum speed of the runner.
            image (pygame.Surface): The image of the runner.
            lives (int): The number of lives of the runner.
        """
        super().__init__(position, size, speed, image, lives)

        self.take_damage = True

    def update(self) -> None:
        """
        Updates the runner enemy with every frame.
        """
        self.apply_gravity()
        self.move_and_check_collisions()
        self.check_boundaries()
        self.check_alive()
