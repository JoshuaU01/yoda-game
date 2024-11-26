from typing import Optional

import pygame

from src.asset import Asset
from src.assets.objects.health_bar import HealthBar
from src.environment.world import World


class Character(Asset):
    """
    A super class for all players and enemies.
    """

    @property
    def collision(self) -> list[Asset]:
        """
        All found collisions to any other character, border or block

        Returns:
            list[Asset]: The assets that collided with the character
        """
        combined_sprites = (
                World.players.sprites() + World.enemies.sprites() + World.borders.sprites() +
                World.blocks.sprites())  # A list is way faster than a separate group
        if self in combined_sprites:
            combined_sprites.remove(self)

        return pygame.sprite.spritecollide(self, combined_sprites, False, pygame.sprite.collide_rect)

    @property
    def precise_collision(self):
        collisions = self.collision
        return pygame.sprite.spritecollideany(self, collisions, pygame.sprite.collide_mask)

    def __init__(
            self, position: tuple[int, int], size: tuple[int, int], speed: int, image: pygame.Surface,
            health: int = 1000, sprite_groups: Optional[list[pygame.sprite.Group]] = None) -> None:
        """
        Creates an instance of this class.

        Args:
            position (tuple[int, int]): The position of the top left corner of the character.
            size (tuple[int, int]): The size of the character.
            speed (int): The maximum speed of the character.
            image (pygame.Surface): The image of the character.
            health (int): The number of lives of the character.
            sprite_groups: (Optional[list[pygame.sprite.Group]]): The global sprite groups that the character will be
            put in during initialization.
        """
        super().__init__(sprite_groups=sprite_groups)
        self.image = pygame.transform.scale(image, (size[0], size[1]))
        self.rect = self.image.get_rect()
        self.rect.topleft = (position[0], position[1])
        self.mask = pygame.mask.from_surface(self.image)

        self.velocity = pygame.math.Vector2()
        self.on_ground = False
        self.speed = speed

        self.health = health
        self.health_bar = HealthBar(self)

    def update_position_x(self) -> None:
        """
        Calculates the new horizontal position of the character with respect to collisions.
        """
        old_x = self.rect.x
        self.rect.x += self.velocity.x
        if self.precise_collision:
            self.rect.x = old_x

    def update_position_y(self) -> None:
        """
        Calculates the new vertical position of the character with respect to collisions.
        """
        old_y = self.rect.y
        self.rect.y += self.velocity.y
        if collisions_y := self.precise_collision:
            if self.velocity.y > 0:
                # self.rect.bottom = collisions_y.rect.top
                self.rect.y = old_y
                self.velocity.y = 0
                self.on_ground = True
            elif self.velocity.y < 0:
                # self.rect.top = collisions_y.rect.bottom
                self.rect.y = old_y
                self.velocity.y = 0
        else:
            self.on_ground = False

    def lose_health(self, amount: int) -> None:
        """
        Decreases the number of lives of the character.

        Args:
            amount (int): The amount lost lives.
        """
        self.health -= amount

    def check_boundaries(self) -> None:
        """
        Practically kills a character who fell out of the world.
        """
        if self.rect.top > (12 / 10) * World.SCREEN_HEIGHT:
            self.lose_health(1000)

    def check_alive(self) -> bool:
        """
        Decides, if the character has enough health to be allowed to live.

        Returns:
            bool: Whether the character is still alive or not.
        """
        if self.health <= 0:
            print(f"{self.__str__()} has died.")
            self.kill()
            return False
        return True
