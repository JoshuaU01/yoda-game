from typing import Optional

import pygame

from src.asset import Asset
from src.environment.world import World


class Character(Asset):
    """
    A super class for all players and enemies.
    """

    def __init__(
            self, position: tuple[int, int], size: tuple[int, int], speed: int, image: pygame.Surface,
            lives: int = 1000) -> None:
        """
        Creates an instance of this class.

        Args:
            position (tuple[int, int]): The position of the top left corner of the character.
            size (tuple[int, int]): The size of the character.
            speed (int): The maximum speed of the character.
            image (pygame.Surface): The image of the character.
            lives (int): The number of lives of the character.
        """
        super().__init__()
        self.image = pygame.transform.scale(image, (size[0], size[1]))
        self.rect = self.image.get_rect()
        self.rect.topleft = (position[0], position[1])
        self.velocity = pygame.math.Vector2()

        self.speed = speed
        self.lives = lives

    @property
    def collision(self) -> Optional[Asset]:
        """
        The first found collision to any other character, border or block

        Returns:
            Optional[Asset]: The asset that collided with the character
        """
        sprites_to_be_checked = [sprite for sprite in
                                 (World.players.sprites() + World.enemies.sprites() + World.borders.sprites() +
                                  World.blocks.sprites()) if sprite != self]
        return pygame.sprite.spritecollideany(self, sprites_to_be_checked)

    def update_position_x(self) -> None:
        """
        Calculates the new horizontal position of the character with respect to collisions.
        """
        old_x = self.rect.x
        self.rect.x += self.velocity.x
        if self.collision:
            self.rect.x = old_x

    def update_position_y(self) -> None:
        """
        Calculates the new vertical position of the character with respect to collision.
        """
        self.rect.y += self.velocity.y
        if collision_y := self.collision:
            if self.velocity.y > 0:
                self.rect.bottom = collision_y.rect.top
                self.velocity.y = 0
                self.on_ground = True
            elif self.velocity.y < 0:
                self.rect.top = collision_y.rect.bottom
                self.velocity.y = 0
        else:
            self.on_ground = False

    def lose_lives(self, amount: int) -> None:
        """
        Decreases the number of lives of the character.

        Args:
            amount (int): The amount lost lives.
        """
        self.lives -= amount

    def check_boundaries(self) -> None:
        """
        Practically kills a character who fell out of the world.
        """
        if self.rect.top > (12 / 10) * World.SCREEN_HEIGHT:
            self.lose_lives(1000)

    def check_alive(self) -> bool:
        """
        Decides, if the character has enough lives to be allowed to live.

        Returns:
            bool: Whether the character is still alive or not.
        """
        if self.lives <= 0:
            print(f"{self.__str__()} has died.")
            self.kill()
            return False
        return True
