from __future__ import annotations
from typing import Optional

import pygame

from src.environment.world import World


class Asset(pygame.sprite.Sprite):
    """
    A super class for all entities, objects, etc.
    """

    def __init__(self, sprite_groups: Optional[list[pygame.sprite.Group]] = None) -> None:
        """
        Creates an instance of this class.

        Args:
            sprite_groups: (Optional[list[pygame.sprite.Group]]): The global sprite groups that the asset will be put
            in during initialization.
        """
        if sprite_groups is None:
            sprite_groups = []
        super().__init__(*sprite_groups)
        self.rect = pygame.Rect(0, 0, 0, 0)  # Placeholder
        self.visible = True

    def is_near(self, asset: Asset, distance: tuple[int | float, int | float]) -> bool:  # TODO use masks
        """
        Checks, if an asset is near the asset.

        Args:
            asset (Optional[Asset]): The asset to check.
            distance (tuple[int | float, int | float]): The semi-axles of the elliptic area that is considered near.

        Returns:
            bool: Whether the asset is near the asset.
        """
        return ((self.rect.centerx - asset.rect.centerx) ** 2 / distance[0] ** 2) + (
                (self.rect.centery - asset.rect.centery) ** 2 / distance[1] ** 2) <= 1
