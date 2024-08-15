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
            detection_range (int): The range of an area that a runner can detect an asset in.
        """
        super().__init__(position, size, speed, image, lives)

        self.direction = Directions.RIGHT
        self.take_damage = True

        self.state = self.walk
        self.target = None
        self.detection_range = detection_range
        self.delay = 20

    def update(self) -> None:
        """
        Updates the runner enemy with every frame.
        """
        self.apply_gravity()
        self.state = self.determine_state()
        self.state()
        self.update_position_x()
        self.update_position_y()
        self.check_boundaries()
        self.check_alive()

    def is_near(self, asset: Asset) -> bool:
        """
        Checks, if an asset is near the runner.

        Args:
            asset (Optional[Asset]): The asset to check.

        Returns:
            bool: Whether the asset is near the runner.
        """
        elliptic_distance = math.sqrt((self.rect.x - asset.rect.x) ** 2 + 2 * (self.rect.y - asset.rect.y) ** 2)
        if elliptic_distance <= self.detection_range:
            return True
        return False

    def look_for_players(self) -> Optional[Player]:
        """
        Checks, if any player is within the detection range of the runner.

        Returns:
            Optional[Player]: A near player.
        """
        for player in World.players:
            if self.is_near(player):
                return player
        return None

    def face_target(self, target: Asset) -> None:
        """
        The runner orients himself towards his target.

        Args:
            target (Asset): The target of the runner.
        """
        if (target.rect.x - self.rect.x) * self.direction >= 0:  # Runner is facing the target
            self.delay = 20  # Reset delay
        else:  # Runner is facing the opposite direction of the target
            if self.delay <= 0:
                self.direction *= -1  # Turn around
                self.image = pygame.transform.flip(self.image, True, False)
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
        if self.target and self.is_near(self.target):
            return self.run
        self.target = self.look_for_players()
        if self.target:
            return self.run
        return self.walk
