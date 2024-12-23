import pygame

from src.assets.characters.enemy import Enemy
from src.assets.objects.bullet import Bullet
from src.environment.world import World, Directions


class SniperGuy(Enemy):
    """
    A long-range combat enemy type that can run towards the player.
    """

    def __init__(
            self,
            position: tuple[int, int],
            size: tuple[int, int],
            speed: int,
            image: pygame.Surface,
            direction: Directions,
            bullet_speed: int,
            bullet_TTL: int,
            health: int,
            can_take_damage: bool = True) \
            -> None:
        """
        Creates an instance of this class.

        Args:
            position (tuple[int, int]): The position of the top left corner of the sniper guy.
            size (tuple[int, int]): The size of the sniper guy.
            speed (int): The maximum speed of the sniper guy.
            image (pygame.Surface): The image of the sniper guy.
            health (int): The number of lives of the sniper guy.
            can_take_damage (bool): Whether the sniper guy can take damage.
        """
        super().__init__(position, size, speed, image, direction, health, can_take_damage=can_take_damage)

        self.bullets = pygame.sprite.Group()
        self.bullet_speed = bullet_speed
        self.bullet_TTL = bullet_TTL
        self.cooldown = 20

    def update(self) -> None:
        """
        Updates the sniper guy enemy with every frame.
        """
        self.shoot()
        self.apply_gravity()
        self.update_position_x()
        self.update_position_y()
        self.apply_cooldown()
        self.check_boundaries()
        self.check_alive()
        self.animate()

    def shoot(self) -> None:
        """
        Lets the sniper guy shoot bullets.
        """
        if self.cooldown <= 0:
            bullet = Bullet(
                self, (self.rect.x, self.rect.y + (2 / 5) * self.rect.height), (int(self.bullet_speed / 1.3), 4),
                self.bullet_speed, Directions.LEFT, time_to_live=self.bullet_TTL)
            self.bullets.add(bullet)
            self.cooldown = 120

    def apply_cooldown(self) -> None:
        """
        Counts down a timer for the next allowed shot.
        """
        if self.cooldown > 0:
            self.cooldown -= 1
