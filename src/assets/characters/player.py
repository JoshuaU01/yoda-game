import pygame

from src.assets.character import Character
from src.assets.objects.bullet import Bullet
from src.environment.world import World, Directions


class Player(Character):
    """
    A class for the player.
    """

    def __init__(
            self,
            position:
            tuple[int, int],
            size: tuple[int, int],
            speed: int,
            image: pygame.Surface,
            direction: Directions,
            health: int,
            can_take_damage: bool = True) \
            -> None:
        """
        Creates an instance of this class.

        Args:
            position (tuple[int, int]): The position of the top left corner of the player.
            size (tuple[int, int]): The size of the player.
            speed (int): The maximum speed of the player.
            image (pygame.Surface): The image of the player.
            health (int): The number of lives of the player.
            can_take_damage (bool): Whether the player can take damage.
        """
        sprite_groups = [World.all_sprites, World.players]
        super().__init__(
            position, size, speed, image, direction, health=health, can_take_damage=can_take_damage,
            sprite_groups=sprite_groups)

        self.is_jumping = False
        self.jump_strength = 20
        self.jump_cooldown = 0

        self.bullets = pygame.sprite.Group()
        self.shoot_cooldown = 0

    def update(self) -> None:
        """
        Updates the player with every frame.
        """
        self.handle_input()
        self.apply_gravity()
        self.update_position_x()
        self.update_position_y()
        self.apply_shoot_cooldown()
        self.check_boundaries()
        self.check_alive()
        self.animate()

    def handle_input(self) -> None:
        """
        Detects the key inputs and triggers actions from them.
        """
        keys = pygame.key.get_pressed()
        self.velocity.x = 0
        if keys[pygame.K_LEFT]:
            self.velocity.x = - self.speed
            self.direction = Directions.LEFT
        if keys[pygame.K_RIGHT]:
            self.velocity.x = self.speed
            self.direction = Directions.RIGHT
        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump()
        if keys[pygame.K_a]:
            self.shoot()

    def jump(self) -> None:
        """
        Starts a jump.
        """
        self.velocity.y = -self.jump_strength
        self.is_jumping = True

    def shoot(self) -> None:
        """
        Lets the player shoot bullets.
        """
        if self.shoot_cooldown <= 0:
            if len(self.bullets) < 3:
                bullet = Bullet(
                    self, (self.rect.x + self.rect.width * (1 / 2) * (self.direction + 1) + self.direction * 15,
                           self.rect.y + self.rect.height * (2 / 3)), (12, 12), 12, self.direction)
                self.bullets.add(bullet)
                self.shoot_cooldown = 20

    def apply_shoot_cooldown(self) -> None:
        """
        Counts down a timer for the next allowed shot.
        """
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def check_alive(self) -> None:
        """
        Decides, if the character has enough health to be allowed to live.
        """
        alive = super().check_alive()
        if not alive:
            World.RUNNING = False
