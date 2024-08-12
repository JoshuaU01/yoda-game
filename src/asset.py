import pygame


class Asset(pygame.sprite.Sprite):
    """
    A super class for all entities, objects, etc.
    """

    def __init__(self) -> None:
        """
        Creates an instance of this class.
        """
        super().__init__()
        self.rect = pygame.Rect(0, 0, 0, 0)  # Placeholder
