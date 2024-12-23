from __future__ import annotations
from typing import Optional

import pygame

from src.environment.world import World


class Asset(pygame.sprite.Sprite):
    """
    A super class for all entities, objects, etc.
    """

    @property
    def collision(self) -> list[Asset]:
        """
        All found collisions to any other character, border or block

        Returns:
            list[Asset]: The assets that collided with the asset
        """
        combined_sprites = (
                World.players.sprites() + World.enemies.sprites() + World.borders.sprites() +
                World.blocks.sprites())  # A list is way faster than a separate sprite group
        if self in combined_sprites:
            combined_sprites.remove(self)

        return pygame.sprite.spritecollide(self, combined_sprites, False, pygame.sprite.collide_rect)

    @property
    def precise_collision(self) -> list[Asset]:
        """
        Uses masks instead of rects for collision check.

        Returns:
            list[Asset]: The assets that collided with the asset
        """
        collisions = self.collision
        return pygame.sprite.spritecollide(self, collisions, False, pygame.sprite.collide_mask)

    @property
    def precise_collision_with_coords(self) -> list[tuple[Asset, tuple[int, int]]]:
        """
        Mask based collision check. Also returns the collision coordinates.

        Returns:
            list[tuple[Asset, tuple[int, int]]]: A combined list of the collided assets and the collision coordinates.
        """
        precise_collisions = self.precise_collision
        collision_coordinates = [pygame.sprite.collide_mask(self, collided_asset) for collided_asset in
                                 precise_collisions]
        return list(zip(precise_collisions, collision_coordinates))

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
        self.hitbox_visible = World.hitboxes_visible

        self.can_take_damage = False  # Placeholder

    def toggle_hitbox_visibility(self) -> None:
        """
        Toggles the visibility of the hitbox of the asset.
        """
        self.hitbox_visible = not self.hitbox_visible

    def is_near(self, asset: Asset, distance: tuple[int | float, int | float]) -> bool:  # TODO use masks
        """
        Checks, if an asset is near the asset.

        Args:
            asset (Optional[Asset]): The asset to check.
            distance (tuple[int | float, int | float]): The semi-axles of the elliptic area that is considered near.

        Returns:
            bool: Whether the asset is near the asset.
        """
        if distance[0] <= 0 or distance[1] <= 0:
            return False
        return ((self.rect.centerx - asset.rect.centerx) ** 2 / distance[0] ** 2) + (
                (self.rect.centery - asset.rect.centery) ** 2 / distance[1] ** 2) <= 1
