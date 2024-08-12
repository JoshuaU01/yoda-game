from typing import Tuple

import pygame

from character import Character
from bullet import Bullet
from world import World

from colors import *
from screen_dimensions import *
from directions import *


class Player(Character):
    """
    A class for the player.
    """

    def __init__(
            self, position: Tuple[int, int], size: Tuple[int, int], speed: int, image: pygame.Surface,
            lives: int = 10) -> None:
        """
        Creates an instance of this class.

        Args:
            position (Tuple[int, int]): The position of the top left corner of the player.
            size (Tuple[int, int]): The size of the player.
            speed (int): The maximum speed of the player.
            image (pygame.Surface): The image of the player.
            lives (int): The number of lives of the player.
        """
        super().__init__(position, size, speed, image, lives)

        self.is_jumping = False
        self.gravity = 1.3
        self.jump_strength = 20
        self.on_ground = False

        self.direction = RIGHT
        self.jump_cooldown = 0

        self.take_damage = True
        self.bullets = pygame.sprite.Group()
        self.cooldown = 0

    def update(self) -> None:
        """
        Updates the player with every frame.
        """
        self.handle_input()
        self.apply_gravity()
        self.move_and_check_collisions()
        self.apply_cooldown()
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
            if self.direction == RIGHT:
                self.image = pygame.transform.flip(self.image, True, False)
            self.direction = LEFT
        if keys[pygame.K_RIGHT]:
            self.velocity.x = self.speed
            if self.direction == LEFT:
                self.image = pygame.transform.flip(self.image, True, False)
            self.direction = RIGHT
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

    def move_and_check_collisions(self) -> None:
        """
        Calculates the new position of the player with respect to their movement and other assets.
        """
        old_rect = self.rect.copy()

        # Check for collision in horizontal direction
        self.rect.x += self.velocity.x
        if pygame.sprite.spritecollideany(self, World.enemies) or pygame.sprite.spritecollideany(
                self, World.borders) or pygame.sprite.spritecollideany(
            self, World.blocks):
            self.rect.x = old_rect.x

        # Check for collision in vertical direction
        self.rect.y += self.velocity.y
        collision_enemy = pygame.sprite.spritecollideany(self, World.enemies)
        collision_border = pygame.sprite.spritecollideany(self, World.borders)
        collision_block = pygame.sprite.spritecollideany(self, World.blocks)

        # TODO reduce code complexity
        if collision_enemy:
            if self.velocity.y > 0:
                self.rect.bottom = collision_enemy.rect.top
                self.velocity.y = 0
                self.on_ground = True
            elif self.velocity.y < 0:
                self.rect.top = collision_enemy.rect.bottom
                self.velocity.y = 0
        elif collision_border:
            self.rect.bottom = collision_border.rect.top
            self.velocity.y = 0
            self.on_ground = True

            # self.rect.y = old_rect.y
            # self.on_ground = True
            # self.velocity.y = 0
            # if self.rect.bottom > collision_border.rect.top:
            #    self.rect.bottom = collision_border.rect.top
        elif collision_block:
            if self.velocity.y > 0:
                self.rect.bottom = collision_block.rect.top
                self.velocity.y = 0
                self.on_ground = True
            elif self.velocity.y < 0:
                self.rect.top = collision_block.rect.bottom
                self.velocity.y = 0
        else:
            self.on_ground = False

    def shoot(self) -> None:
        """
        Lets the player shoot bullets.
        """
        if self.cooldown <= 0:
            if len(self.bullets) < 5:
                bullet = Bullet(
                    (self.rect.x + self.rect.width * (1 / 2) * (self.direction + 1),
                     self.rect.y + self.rect.height * (2 / 3)), (12, 12), 12, self.direction)
                self.bullets.add(bullet)
                World.all_sprites.add(bullet)
                self.cooldown = 8

    def apply_cooldown(self) -> None:
        """
        Counts down a timer for the next allowed shot.
        """
        if self.cooldown > 0:
            self.cooldown -= 1

    def check_alive(self) -> None:
        """
        Decides, if the character has enough lives to be allowed to live.
        """
        alive = super().check_alive()
        if not alive:
            World.RUNNING = False
