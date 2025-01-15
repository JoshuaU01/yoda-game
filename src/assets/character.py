from typing import Optional

from abc import ABC, abstractmethod
import pygame

from src.asset import Asset
from src.assets.objects.health_bar import HealthBar
from src.environment.world import World, Directions
from src.utils import counter


class Character(Asset, ABC):
    """
    A super class for all players and enemies.
    """

    @property
    def on_ground(self) -> bool:
        """
        Checks whether the character stands on a solid asset.
        This works by checking if the character would have collisions if they stood 1 pixel lower.

        Returns:
            bool: True if the character stands on something.
        """
        self.rect.y += 1
        collision = self.collision
        self.rect.y -= 1
        if collision:
            return True
        return False

    def __str__(self) -> str:
        """
        Overrides the default __str__ method.

        Returns:
            str: Includes the class name and the character's coordinates.
        """
        return f"{self.__class__.__name__} at {self.rect.topleft}"

    @abstractmethod
    def __init__(
            self,
            position: tuple[int, int],
            size: tuple[int, int],
            speed: int,
            image: pygame.Surface,
            direction: Directions,
            health: int = 1000,
            can_take_damage: bool = True,
            sprite_groups: Optional[list[pygame.sprite.Group]] = None) \
            -> None:
        """
        Creates an instance of this class.

        Args:
            position (tuple[int, int]): The position of the top left corner of the character.
            size (tuple[int, int]): The size of the character.
            speed (int): The maximum speed of the character.
            image (pygame.Surface): The image of the character.
            direction (Directions): The initial horizontal direction the character is facing.
            health (int): The number of lives of the character.
            can_take_damage (bool): Whether the character can take damage.
            sprite_groups: (Optional[list[pygame.sprite.Group]]): The global sprite groups that the character will be
            put in during initialization.
        """
        super().__init__(sprite_groups=sprite_groups)
        self.image = pygame.transform.smoothscale(image, (size[0], size[1]))
        self.original_image = self.image.copy()
        self.rect = self.image.get_rect()
        self.rect.topleft = (position[0], position[1])
        self.mask = pygame.mask.from_surface(self.image)
        self.direction = direction

        self.velocity = pygame.math.Vector2()
        self.speed = speed
        self.gravity = 1.3

        self.health = health
        self.health_bar = HealthBar(self)
        self.can_take_damage = can_take_damage
        self.receiving_damage = False
        self.damage_indicator_counter = counter.up_and_down(10)

    def update_position_x(self) -> None:
        """
        Calculates the new horizontal position of the character with respect to collisions.
        """
        self.rect.x += self.velocity.x
        if collisions_x := self.collision:
            collided_asset = collisions_x[0]
            if self.velocity.x > 0:  # Moving right
                self.rect.right = collided_asset.rect.left
                self.velocity.x = 0
            elif self.velocity.x < 0:  # Moving left
                self.rect.left = collided_asset.rect.right
                self.velocity.x = 0

    def update_position_y(self) -> None:
        """
        Calculates the new vertical position of the character with respect to collisions.
        """
        self.rect.y += self.velocity.y
        if collisions_y := self.collision:
            collided_asset = collisions_y[0]
            if self.velocity.y > 0:  # Moving downwards
                self.rect.bottom = collided_asset.rect.top
                self.velocity.y = 0
            elif self.velocity.y < 0:  # Moving upwards
                self.rect.top = collided_asset.rect.bottom
                self.velocity.y = 0

    def is_facing(self, asset: Asset) -> bool:
        """
        Checks whether the character is facing a specified asset.

        Params:
            asset (Asset): The asset to check.

        Returns:
            bool: True if the character is facing the asset.
        """
        return (asset.rect.x - self.rect.x) * self.direction >= 0

    def turn_around(self) -> None:
        """
        Changes the character's horizontal direction.
        """
        self.direction *= -1

    def apply_gravity(self) -> None:
        """
        Pulls the character down while in the air.
        """
        if not self.on_ground:
            self.velocity.y += self.gravity

    def lose_health(self, amount: int) -> None:
        """
        Decreases the number of lives of the character.

        Args:
            amount (int): The amount lost lives.
        """
        self.health -= amount

    def indicate_damage(self) -> None:
        """
        Enables the light_up method to visually indicate received damage.
        """
        self.receiving_damage = True

    def take_damage(self, damage: int) -> None:
        """
        Triggers some methods to process a character's health loss.

        Args:
            damage (int): The amount of health the character loses.
        """
        self.lose_health(damage)
        self.indicate_damage()

    def check_boundaries(self) -> None:
        """
        Practically kills a character who fell out of the world.
        """
        if (self.rect.right < World.boundaries["left"] or
                self.rect.left > World.boundaries["right"] or
                self.rect.bottom < World.boundaries["top"] or
                self.rect.top > World.boundaries["bottom"]):
            self.take_damage(1000)

    def check_alive(self) -> bool:
        """
        Decides whether the character has enough health to be allowed to live.

        Returns:
            bool: True if the character is still alive.
        """
        if self.health <= 0:
            print(f"{self} has died!")
            self.kill()
            return False
        return True

    def light_up(self) -> None:
        """
        Flashes the character's image with red color after receiving damage.
        """
        if self.receiving_damage:
            # Determine intensity of the red overlay color
            intensity = 12 * next(self.damage_indicator_counter)
            if intensity < 0 or intensity > 255:
                print("Color codes must be in [0; 255].")
                intensity = max(0, min(255, intensity))

            # Create and fill color layers
            add_layer = pygame.Surface(self.rect.size, pygame.SRCALPHA)
            norm_layer = pygame.Surface(self.rect.size, pygame.SRCALPHA)
            add_layer.fill((intensity, 0, 0))
            norm_layer.fill((255, 255 - intensity, 255 - intensity))

            # Blit color layers onto the character's image
            self.image.blit(add_layer, (0, 0), special_flags=pygame.BLEND_RGB_ADD)
            self.image.blit(norm_layer, (0, 0), special_flags=pygame.BLEND_RGB_MULT)

            # End the animation
            if intensity <= 0:
                self.receiving_damage = False

    def animate(self) -> None:
        """
        Picks a suitable image based on some status flags of the character.
        """
        # TODO Use temp image and more flags to avoid repeating unnecessary operations?
        self.image = self.original_image.copy()  # Fetch original image
        self.image = pygame.transform.smoothscale(self.image, self.rect.size)  # Scale to hitbox dimensions
        self.image = pygame.transform.flip(self.image, self.direction == Directions.LEFT, False)  # Flip if facing left
        self.mask = pygame.mask.from_surface(self.image)  # Update mask
        self.light_up()  # Display dealt damage
