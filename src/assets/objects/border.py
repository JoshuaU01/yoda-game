import pygame

from src.assets.object import Object


class Border(Object):
    """
    An invisible horizontal or vertical barricade whose purpose is not to be overcome
    """

    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        """
        Creates an instance of this class.

        Args:
            x (int): The horizontal position of the left border of the border.
            y (int): The vertical position of the upper border of the border.
            width (int): The width of the border.
            height (int): The height of the border.
        """
        super().__init__()
        self.image = pygame.Surface([width, height], pygame.SRCALPHA)
        # self.image.fill(Colors.RED)  # Debug purposes
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
