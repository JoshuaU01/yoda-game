import pygame

from src.assets.character import Character
from src.assets.objects.bullet import Bullet
from src.environment.world import World, Directions


class Player(Character):
    """
    A class for the player.
    """

    def __init__(
            self, position: tuple[int, int], size: tuple[int, int], speed: int, image: pygame.Surface,
            health: int = 10) -> None:
        """
        Creates an instance of this class.

        Args:
            position (tuple[int, int]): The position of the top left corner of the player.
            size (tuple[int, int]): The size of the player.
            speed (int): The maximum speed of the player.
            image (pygame.Surface): The image of the player.
            health (int): The number of lives of the player.
        """
        super().__init__(position, size, speed, image, health)
        World.players.add(self)

        self.is_jumping = False
        self.gravity = 1.3
        self.jump_strength = 20

        self.direction = Directions.RIGHT
        self.jump_cooldown = 0

        self.take_damage = True
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

    def handle_input(self) -> None:
        """
        Detects the key inputs and triggers actions from them.
        """
        keys = pygame.key.get_pressed()
        self.velocity.x = 0
        if keys[pygame.K_LEFT]:
            self.velocity.x = - self.speed
            if self.direction == Directions.RIGHT:
                self.image = pygame.transform.flip(self.image, True, False)
            self.direction = Directions.LEFT
        if keys[pygame.K_RIGHT]:
            self.velocity.x = self.speed
            if self.direction == Directions.LEFT:
                self.image = pygame.transform.flip(self.image, True, False)
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
        self.on_ground = False

    def apply_gravity(self) -> None:
        """
        Pulls the player down while in the air.
        """
        if not self.on_ground:
            self.velocity.y += self.gravity

    def shoot(self) -> None:
        """
        Lets the player shoot bullets.
        """
        if self.shoot_cooldown <= 0:
            if len(self.bullets) < 3:
                bullet = Bullet(
                    (self.rect.x + self.rect.width * (1 / 2) * (self.direction + 1),
                     self.rect.y + self.rect.height * (2 / 3)), (12, 12), 12, self.direction)
                self.bullets.add(bullet)
                self.shoot_cooldown = 12

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
