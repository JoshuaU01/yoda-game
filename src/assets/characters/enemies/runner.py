from typing import Optional, Callable

import math
import pygame

from src.asset import Asset
from src.assets.characters.enemy import Enemy
from src.assets.characters.player import Player
from src.environment.world import World, Directions


class Runner(Enemy):
    """
    A melee enemy type that can run towards the player.
    """

    def __init__(
            self,
            position: tuple[int, int],
            size: tuple[int, int],
            speed: int,
            image: pygame.Surface,
            detect_range: tuple[int, int],
            health: int,
            take_damage: bool = True,
            direction: Directions = Directions.RIGHT) \
            -> None:
        """
        Creates an instance of this class.

        Args:
            position (tuple[int, int]): The position of the top left corner of the runner.
            size (tuple[int, int]): The size of the runner.
            speed (int): The maximum speed of the runner.
            image (pygame.Surface): The image of the runner.
            detect_range (tuple[int, int]): The horizontal and vertical range that a runner can detect an asset in.
            health (int): The number of lives of the runner.
            take_damage (bool): Whether the runner can take damage.
            direction (Directions): The horizontal direction the runner is facing.
        """
        super().__init__(position, size, speed, image, health, take_damage=take_damage)

        self.direction = direction
        self.image = pygame.transform.flip(
            self.image, self.direction == Directions.LEFT, False)  # TODO Generalize image flipping
        self.mask = pygame.mask.from_surface(self.image)

        self.state = self.walk
        self.target = None
        self.detect_range = detect_range
        self.attack_range = tuple(x * (2 / 3) for x in self.detect_range)
        self.delay = 20

        self.gravity = 1.2
        self.is_stomping = False
        self.stomp_cooldown = 10

    def update(self) -> None:
        """
        Updates the runner enemy with every frame.
        """
        self.apply_gravity()
        self.state = self.determine_state()
        self.state()
        self.attack()
        self.apply_stomp_cooldown()
        self.update_position_x()
        self.update_position_y()
        self.check_boundaries()
        self.check_alive()

    def is_facing(self, asset: Asset) -> bool:
        """
        Checks, if the runner is facing a specified asset.

        Params:
            asset (Asset): The asset to check.

        Returns:
            bool: Whether the runner is facing the asset.
        """
        return (asset.rect.x - self.rect.x) * self.direction >= 0

    def look_for_players(self) -> Optional[Player]:
        """
        Checks, if any player is within the detection range of the runner.

        Returns:
            Optional[Player]: A near player.
        """
        for player in World.players:
            if self.is_near(player, self.detect_range) and self.is_facing(player):
                return player
        return None

    def face_target(self, target: Asset) -> None:
        """
        The runner orients himself towards his target.

        Args:
            target (Asset): The target of the runner.
        """
        if self.is_facing(target):
            self.delay = 20  # Reset delay
        else:
            if self.delay <= 0:
                self.direction *= -1  # Turn around
                self.image = pygame.transform.flip(self.image, True, False)
                self.mask = pygame.mask.from_surface(self.image)
                self.delay = 20  # Reset delay after turn
            else:
                self.delay -= 1

    def walk(self) -> None:
        """
        Movement type. The runner slowly walks from side to side.
        """
        self.velocity.x = self.direction * self.speed
        old_x = self.rect.x
        self.rect.x += self.velocity.x
        if self.collision:  # Pre-check, if the runner would collide with something.
            self.direction *= -1  # Turn around
            self.velocity.x *= -1
            self.image = pygame.transform.flip(self.image, True, False)
            self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = old_x  # Always reset the horizontal position, as the position update will be done later

    def run(self) -> None:
        """
        Movement type. The runner runs towards his target.
        """
        self.face_target(self.target)
        self.velocity.x = self.direction * self.speed * 3

    def determine_state(self) -> Callable[[], None]:
        """
        Selects a movement type based on the players' behavior.

        Returns:
            Callable[[], None]: A reference to the selected state method.
        """
        if self.target and self.is_near(self.target, self.detect_range):
            return self.run
        self.target = self.look_for_players()
        if self.target:
            return self.run
        return self.walk

    def stomp(self) -> None:
        """
        Starts the stomp attack of the runner.
        """
        if self.on_ground:
            self.velocity.y = -12
            self.on_ground = False
        self.is_stomping = True
        self.stomp_cooldown = 50

    def attack(self) -> None:
        """
        Handles the attack of the runner.
        """
        if self.state == self.run and self.target and self.is_near(
                self.target, self.attack_range) and self.stomp_cooldown <= 0:
            self.stomp()
        if self.is_stomping and self.on_ground:
            if self.target and self.is_near(
                    self.target, (self.attack_range[0], 40)):
                self.target.health -= 1
                print(f"{self.target} got hit!")
            # TODO shake the camera (observer)
            self.is_stomping = False

    def apply_stomp_cooldown(self) -> None:
        """
        Counts down a timer for the next allowed stomp attack.
        """
        if not self.is_stomping and self.stomp_cooldown > 0:
            self.stomp_cooldown -= 1
