import pygame

from asset import Asset

from screen_dimensions import *


class Character(Asset):
    """
    A super class for all players and enemies.
    """

    def __init__(
            self, position: tuple[int, int], size: tuple[int, int], speed: int, image: pygame.Surface,
            lives: int = 1000) -> None:
        """
        Creates an instance of this class.

        Args:
            position (tuple[int, int]): The position of the top left corner of the character.
            size (tuple[int, int]): The size of the character.
            speed (int): The maximum speed of the character.
            image (pygame.Surface): The image of the character.
            lives (int): The number of lives of the character.
        """
        super().__init__()
        self.image = pygame.transform.scale(image, (size[0], size[1]))
        self.rect = self.image.get_rect()
        self.rect.topleft = (position[0], position[1])
        self.velocity = pygame.math.Vector2()

        self.speed = speed
        self.lives = lives

    def lose_lives(self, amount: int) -> None:
        """
        Decreases the number of lives of the character.

        Args:
            amount (int): The amount lost lives.
        """
        self.lives -= amount

    def check_alive(self) -> bool:
        """
        Decides, if the character has enough lives to be allowed to live.

        Returns:
            bool: Whether the character is still alive or not.
        """
        if self.lives <= 0:
            print(f"{self.__str__()} has died.")
            self.kill()
            return False
        return True

    def check_boundaries(self) -> None:
        """
        Practically kills a character who fell out of the world.
        """
        if self.rect.top > (12 / 10) * SCREEN_HEIGHT:
            self.lose_lives(1000)
