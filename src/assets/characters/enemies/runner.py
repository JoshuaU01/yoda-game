from typing import Optional

import pygame

from src.asset import Asset
from src.assets.characters.enemy import Enemy
from src.assets.characters.player import Player
from src.environment.world import World, Directions
from src.utils.state import StateManager, WalkState, RunState, PrepareAttackState, StompState


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
            direction: Directions,
            detect_range: tuple[int, int],
            health: int,
            can_take_damage: bool = True) \
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
            can_take_damage (bool): Whether the runner can take damage.
            direction (Directions): The horizontal direction the runner is facing.
        """
        super().__init__(position, size, speed, image, direction, health, can_take_damage=can_take_damage)

        self.state_manager = StateManager(self)
        self.walk_state = WalkState(self)
        self.run_state = RunState(self)
        self.prepare_attack_state = PrepareAttackState(self)
        self.stomp_state = StompState(self)
        self.state = self.walk_state
        self.target = None
        self.detect_range = detect_range
        self.attack_range = tuple(x * (1 / 3) for x in self.detect_range)
        self.turning_delay = 20

        self.gravity = 1.2
        self.stomp_cooldown = 50

    def update(self) -> None:
        """
        Updates the runner enemy with every frame.
        """
        self.apply_gravity()
        self.target = self.update_target()
        self.state.update()
        self.state.execute()
        self.apply_stomp_cooldown()
        self.update_position_x()
        self.update_position_y()
        self.check_boundaries()
        self.check_alive()
        self.animate()
        print(self.state)

    def is_facing(self, asset: Asset) -> bool:
        """
        Checks, if the runner is facing a specified asset.

        Params:
            asset (Asset): The asset to check.

        Returns:
            bool: Whether the runner is facing the asset.
        """
        return (asset.rect.x - self.rect.x) * self.direction >= 0

    def update_target(self) -> Optional[Player]:
        """
        Checks, if any player is within the detection range of the runner.

        Returns:
            Optional[Player]: A near player.
        """
        if self.target and self.is_near(self.target, self.detect_range):
            return self.target
        for player in World.players:
            if self.is_near(player, self.detect_range) and self.is_facing(player) or self.is_near(
                    player, self.attack_range):
                return player
        return None

    def face_target(self, target: Asset) -> None:
        """
        The runner orients himself towards his target.

        Args:
            target (Asset): The target of the runner.
        """
        if self.is_facing(target):
            self.turning_delay = 20  # Reset turning delay
        else:
            if self.turning_delay <= 0:
                self.direction *= -1  # Turn around
                self.turning_delay = 20  # Reset turning delay after turn
            else:
                self.turning_delay -= 1

    def apply_stomp_cooldown(self) -> None:
        """
        Counts down a timer for the next allowed stomp attack.
        """
        if not self.state == self.stomp_state and self.stomp_cooldown > 0:
            self.stomp_cooldown -= 1
