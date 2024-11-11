from __future__ import annotations

import pygame

from src.environment.world import World


class Asset(pygame.sprite.Sprite):
    """
    A super class for all entities, objects, etc.
    """

    def __init__(self) -> None:
        """
        Creates an instance of this class.
        """
        super().__init__()
        World.all_sprites.add(self)
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
