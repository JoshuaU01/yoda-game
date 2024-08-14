from typing import Optional

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
            self, position: tuple[int, int], size: tuple[int, int], speed: int, image: pygame.Surface,
            lives: int, detection_range: int) -> None:
        """
        Creates an instance of this class.

        Args:
            position (tuple[int, int]): The position of the top left corner of the runner.
            size (tuple[int, int]): The size of the runner.
            speed (int): The maximum speed of the runner.
            image (pygame.Surface): The image of the runner.
            lives (int): The number of lives of the runner.
        """
        super().__init__(position, size, speed, image, lives)

        self.direction = Directions.RIGHT
        self.take_damage = True

        self.target = None
        self.detection_range = detection_range
        self.delay = 20

    def update(self) -> None:
        """
        Updates the runner enemy with every frame.
        """
        self.apply_gravity()
        self.look_for_players()
        self.face_target(self.target)
        self.run()
        print(self.velocity, self.speed)
        self.move_and_check_collisions()
        self.check_boundaries()
        self.check_alive()

    def is_near(self, asset: Optional[Asset]) -> bool:
        """
        Checks, if a player is near the runner.

        Args:
            player (Player): The player to check.

        Returns:
            bool: Whether the player is near the runner.
        """
        if asset:
            distance = math.sqrt((self.rect.x - asset.rect.x) ** 2 + (self.rect.y - asset.rect.y) ** 2)
            if distance <= self.detection_range:
                return True
        return False

    def look_for_players(self) -> None:
        if not self.target or not self.is_near(self.target):
            for player in World.players:
                if self.is_near(player):
                    self.target = player

    def face_target(self, target: Optional[Asset]) -> None:
        if target:
            if (target.rect.x - self.rect.x) * self.direction >= 0:  # Runner is facing the target
                self.delay = 20  # Reset delay
            else:  # Runner is facing the opposite direction of the target
                if self.delay <= 0:
                    self.direction = - self.direction  # Turn around
                    self.delay = 20  # Reset delay after turn
                else:
                    self.delay -= 1

    def run(self) -> None:
        if self.is_near(self.target):
            self.velocity.x = self.direction * self.speed * 3
