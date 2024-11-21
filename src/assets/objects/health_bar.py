from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.assets.character import Character

import pygame
import math

from src.assets.object import Object
from src.environment.world import World


class HealthBar(Object):
    """
    A health bar that can be filled with heart icons to display a character's health.
    """

    def __init__(self, character: "Character") -> None:
        """
        Creates an instance of this class.
        """
        sprite_groups = [World.all_sprites]
        super().__init__(sprite_groups=sprite_groups)
        self.visible = True
        self.character = character
        self.hearts = self.character.health / 2
        self.padding = 1
        self.image = pygame.Surface(
            (math.ceil(self.hearts) * (World.image_full_heart.get_width() + self.padding),
             World.image_full_heart.get_height()), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.character.rect.left, self.character.rect.top - 30
        self.fill()

    def update(self) -> None:
        """
        Updates the health bar with every frame.
        """
        self.update_position()
        previous_hearts = self.hearts
        self.update_hearts()
        # Only draw the health bar, if it changed.
        if self.hearts != previous_hearts:
            self.fill()

    def update_position(self) -> None:
        """
        Updates the position of the health bar with respect to its character's position.
        """
        self.rect.topleft = self.character.rect.left, self.character.rect.top - 30

    def update_hearts(self) -> None:
        """
        Updates the number of hearts of the health bar with respect to its character's health.
        """
        self.hearts = self.character.health / 2

    def fill(self) -> None:
        """
        Actually draws the heart icons onto the health bar.
        """
        self.image.fill((0, 0, 0, 0))  # Clear the health bar.
        # Draw the full hearts onto the health bar.
        for i in range(int(self.hearts)):
            self.image.blit(World.image_full_heart, (i * (World.image_full_heart.get_width() + self.padding), 0))
        # Draw the half heart at the end, if it exists.
        if self.hearts % 1 != 0:
            self.image.blit(
                World.image_half_heart, (int(self.hearts) * (World.image_full_heart.get_width() + self.padding), 0))

    def show(self) -> None:
        """
        Make the health bar visible.
        """
        self.visible = True

    def hide(self) -> None:
        """
        Make the health bar invisible.
        """
        self.visible = False

    def toggle_on_off(self) -> None:
        """
        Toggle visibility of the health bar.
        """
        self.visible = not self.visible
