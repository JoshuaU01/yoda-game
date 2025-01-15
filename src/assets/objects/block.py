import pygame

from src.assets.object import Object


class Block(Object):
    """
    A rectangular object with a hitbox.
    """

    def __init__(self, image: pygame.Surface, x: int, y: int, width: int, height: int) -> None:
        """
        Creates an instance of this class.

        Args:
            image (pygame.Surface): The image of the block.
            x (int): The horizontal position of the left border of the block.
            y (int): The vertical position of the upper border of the block.
            width (int): The width of the block.
            height (int): The height of the block.
        """
        super().__init__()
        self.image = pygame.transform.smoothscale(image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.mask = pygame.mask.from_surface(self.image)
