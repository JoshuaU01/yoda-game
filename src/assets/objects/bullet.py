import pygame

from src.assets.character import Character
from src.assets.object import Object
from src.environment.world import World


class Bullet(Object):
    """
    A projectile that entities can shoot to deal damage to other entities.
    """

    def __init__(
            self, owner: Character, position: tuple[float, float], size: tuple[int, int], speed: int,
            direction: int) -> None:
        """
        Creates an instance of this class.

        Args:
            owner (Character): The originator of the bullet who fired it.
            position (tuple[float, float]): The position of the center of the bullet.
            size (tuple[int, int]): The size of the bullet.
            speed (int): The speed of the bullet.
            direction (int): The shoot direction of the bullet.
        """
        sprite_groups = [World.all_sprites]
        super().__init__(sprite_groups=sprite_groups)
        self.owner = owner
        self.image = pygame.transform.scale(World.images["bullet"], (size[0], size[1]))
        self.rect = self.image.get_rect()
        self.rect.center = (position[0], position[1])
        self.mask = pygame.mask.from_surface(self.image)
        self.velocity = pygame.math.Vector2(0, 0)

        self.speed = speed
        self.direction = direction
        self.TTL = 80

    def update(self) -> None:
        """
        Updates the object with every frame.
        """
        self.move()
        self.check_collisions()
        self.check_TTL()

    def move(self) -> None:
        """
        Makes the bullet move with a certain speed into a given direction.
        """
        self.velocity.x = self.speed * self.direction
        self.rect.x += self.velocity.x
        # self.rect.y += self.velocity.y  # TODO work out self.dirction as vector 1x2?

    def check_collisions(self) -> None:
        """
        Checks collisions with other assets and carries out actions.
        """
        collisions = self.precise_collision
        if collisions:
            for collided_asset in collisions:
                if collided_asset.take_damage and hasattr(
                        collided_asset, "lose_health") and collided_asset is not self.owner:
                    collided_asset.lose_health(1)  # Only vulnerable assets take damage
            self.kill()

    def check_TTL(self) -> None:
        """
        Destroys the bullet after a certain time.
        """
        self.TTL -= 1
        if self.TTL <= 0:
            self.kill()
