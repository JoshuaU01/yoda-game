import pygame

from src.assets.object import Object
from src.environment.world import World


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
        sprite_groups = [World.all_sprites, World.borders]
        super().__init__(sprite_groups=sprite_groups)
        self.image = pygame.Surface([width, height], pygame.SRCALPHA)
        # self.image.fill(Colors.RED)  # Debug purposes
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
