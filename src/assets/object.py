from typing import Optional

from abc import ABC, abstractmethod
import pygame

from src.asset import Asset


class Object(Asset, ABC):
    """
    A super class for all types of objects like blocks, borders, etc.
    """

    @abstractmethod
    def __init__(self, sprite_groups: Optional[list[pygame.sprite.Group]] = None) -> None:
        """
        Creates an instance of this class.

        Args:
            sprite_groups: (Optional[list[pygame.sprite.Group]]): The global sprite groups that the object will be
            put in during initialization.
        """
        super().__init__(sprite_groups=sprite_groups)
        self.can_take_damage = False
