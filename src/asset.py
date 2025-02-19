from __future__ import annotations
from typing import Optional

from abc import ABC, abstractmethod
import pygame

from src.environment.world import World, Colors


class Asset(pygame.sprite.Sprite, ABC):
    """
    A super class for all entities, objects, etc.
    """

    @property
    def collision(self) -> list[Asset]:
        """
        All found collisions to any other character, border or block.
        Uses rects for collision check.

        Returns:
            list[Asset]: The assets that collided with the asset
        """
        combined_sprites = (
                World.players.sprites() + World.enemies.sprites() + World.borders.sprites() +
                World.blocks.sprites())  # A tuple is way faster than a separate sprite group
        if self in combined_sprites:
            combined_sprites.remove(self)

        return pygame.sprite.spritecollide(self, combined_sprites, False, pygame.sprite.collide_rect)

    @property
    def precise_collision(self) -> list[Asset]:
        """
        All found collisions to any other character, border or block.
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

    @abstractmethod
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
        # Placeholder variables
        self.image = pygame.Surface((0, 0))
        self.image.fill(Colors.BLACK)
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.mask = pygame.mask.from_surface(self.image)
        self.can_take_damage = False
        self.visible = True

        self.hitbox_visible = World.hitboxes_visible

    def show(self) -> None:
        """
        Makes the asset visible.
        """
        self.visible = True

    def hide(self) -> None:
        """
        Makes the asset invisible.
        """
        self.visible = False

    def toggle_visibility(self) -> None:
        """
        Toggles the visibility of the asset.
        """
        self.visible = not self.visible

    def toggle_hitbox_visibility(self) -> None:
        """
        Toggles the visibility of the hitbox of the asset.
        """
        self.hitbox_visible = not self.hitbox_visible
