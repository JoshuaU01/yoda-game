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

        self.jump_strength = 20
        self.jump_cooldown = 0
        self.jump_lock = False

        self.bullets = pygame.sprite.Group()
        self.shoot_cooldown = 0
        self.shoot_lock = False

    def update(self) -> None:
        """
        Updates the player with every frame.
        """
        self.handle_input()
        self.apply_gravity()
        self.update_position_x()
        self.update_position_y()
        self.apply_jump_cooldown()
        self.apply_shoot_cooldown()
        self.check_boundaries()
        self.check_alive()
        self.animate()

    def handle_input(self) -> None:
        """
        Detects the key inputs and triggers actions from them.
        """
        # Get key inputs
        keys = pygame.key.get_pressed()

        # Handle walking
        self.velocity.x = 0
        if keys[pygame.K_LEFT]:
            self.velocity.x = - self.speed
            self.direction = Directions.LEFT
        if keys[pygame.K_RIGHT]:
            self.velocity.x = self.speed
            self.direction = Directions.RIGHT

        # Handle jumping
        if keys[pygame.K_SPACE] and self.jump_allowed:
            self.jump()
        elif not keys[pygame.K_SPACE] and self.jump_lock:
            self.jump_lock = False  # Once the jump key is released, the player can jump again

        # Handle shooting
        if keys[pygame.K_a] and self.shoot_allowed:
            self.shoot()
        elif not keys[pygame.K_a] and self.shoot_lock:
            self.shoot_lock = False  # Once the shoot key is released, the player can shoot again

    @property
    def jump_allowed(self) -> bool:
        """
        Whether the player shall be allowed to do a jump.

        Returns:
            bool: True if the player can jump.
        """
        return self.on_ground and self.jump_cooldown <= 0 and not self.jump_lock

    def jump(self) -> None:
        """
        Starts a jump.
        """
        self.velocity.y = -self.jump_strength
        self.jump_cooldown = 15
        self.jump_lock = True

    def apply_jump_cooldown(self) -> None:
        """
        Counts down a timer for the next allowed jump.
        """
        if self.jump_cooldown > 0:
            self.jump_cooldown -= 1

    @property
    def shoot_allowed(self) -> bool:
        """
        Whether the player shall be allowed to fire a shot.

        Returns:
            bool: True if the player can shoot.
        """
        return len(self.bullets) < 3 and self.shoot_cooldown <= 0 and not self.shoot_lock

    def shoot(self) -> None:
        """
        Lets the player shoot bullets.
        """
        bullet = Bullet(
            self, (self.rect.x + self.rect.width * (1 / 2) * (self.direction + 1) + self.direction * 15,
                   self.rect.y + self.rect.height * (2 / 3)), (12, 12), 12, self.direction, time_to_live=30)
        self.bullets.add(bullet)
        self.shoot_cooldown = 25
        self.shoot_lock = True

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
