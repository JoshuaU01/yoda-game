from typing import Optional

import pygame

from src.assets.characters.enemy import Enemy
from src.assets.characters.player import Player
from src.environment.world import World, Directions, Colors
from src.utils.state import State, StateManager
from src.assets.objects.zone import EllipticZone, SemiEllipticZone


class Runner(Enemy):
    """
    A melee enemy type that can run towards the player.
    """

    @property
    def state(self):
        return self.state_manager.current_state

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
        self.state_manager.add_state(WalkState(), state_name="walk", active=True)
        self.state_manager.add_state(RunState(), state_name="run")
        self.state_manager.add_state(PrepareAttackState(), state_name="prepare_attack")
        self.state_manager.add_state(StompState(), state_name="stomp")
        self.target = None
        self.target_lost_counter = 0
        self.detect_zone = EllipticZone(
            self, 2 * detect_range[0], 2 * detect_range[1], color=Colors.GREEN_TRANSPARENT)
        self.attack_zone = EllipticZone(
            self, (1 / 3) * 2 * detect_range[0], 2 * detect_range[1], color=Colors.YELLOW_TRANSPARENT)
        self.continue_attack_zone = EllipticZone(
            self, (1 / 2) * 2 * detect_range[0], 2 * detect_range[1], color=Colors.BLUE_TRANSPARENT)
        self.hit_zone = SemiEllipticZone(
            self, (2 / 3) * 2 * detect_range[0], (1 / 5) * 2 * detect_range[1],
            offset=(0, -((1 / 5) * 2 * detect_range[1] - self.rect.height) / 2), color=Colors.RED_TRANSPARENT)

        self.gravity = 1.2
        self.turning_delay = 15
        self.stomp_cooldown = 50

    def update(self) -> None:
        """
        Updates the runner enemy with every frame.
        """
        self.apply_gravity()
        self.target = self.update_target()
        self.state_manager.update()
        self.state_manager.execute()
        self.apply_stomp_cooldown()
        self.update_position_x()
        self.update_position_y()
        self.check_boundaries()
        self.check_alive()
        self.animate()

    def update_target(self) -> Optional[Player]:
        """
        If the runner has no target, he will search for a near player in the world.
        If the target is still in range, the runner keeps the target,
        even if the target gets out of his range for a short time (self.target_lost_counter).
        If the counter exceeds a certain threshold,
        the runner looses his target and starts searching for a near player again.

        Returns:
            Optional[Player]: A near player.
        """
        # Check if the current target will remain
        if self.target:
            if self.detect_zone.contains(self.target) or self.attack_zone.contains(self.target):
                self.target_lost_counter = 0  # Reset the counter
                return self.target
            else:
                self.target_lost_counter += 1  # Increment the counter for each frame the target is out of range
                if self.target_lost_counter < 40:
                    return self.target

        # Search for other players
        for player in World.players:
            if self.detect_zone.contains(player) and self.is_facing(player) or self.attack_zone.contains(player):
                self.target_lost_counter = 0
                return player
        return None

    def face_target(self) -> None:
        """
        The runner orients himself towards his target.
        """
        if not self.target:
            print(f"{self.__class__.__name__} has no target.")
            return None
        if self.is_facing(self.target):
            self.turning_delay = 15  # Reset turning delay
        elif self.turning_delay <= 0:
            self.turn_around()
            self.turning_delay = 15  # Reset turning delay after turn
        else:
            self.turning_delay -= 1

    def apply_stomp_cooldown(self) -> None:
        """
        Counts down a timer for the next allowed stomp attack.
        """
        if not isinstance(self.state, StompState) and self.stomp_cooldown > 0:
            self.stomp_cooldown -= 1


class WalkState(State):

    @property
    def runner(self):
        return self.state_manager.owner

    def update(self) -> None:
        if self.runner.target:
            if self.runner.attack_zone.contains(self.runner.target):
                self.state_manager.change_state("prepare_attack")  # Transition T5
            else:
                self.state_manager.change_state("run")  # Transition T1

    def execute(self) -> None:
        self.runner.velocity.x = self.runner.direction * self.runner.speed
        old_x = self.runner.rect.x  # Save the current horizontal position
        self.runner.rect.x += self.runner.velocity.x
        if self.runner.collision:  # Pre-check, if the owner would collide with something
            self.runner.turn_around()
            self.runner.velocity.x *= -1  # Walk into the other direction
        self.runner.rect.x = old_x  # Always reset the horizontal position, as the position update will be done later


class RunState(State):

    @property
    def runner(self):
        return self.state_manager.owner

    def update(self):
        if not self.runner.target:
            self.state_manager.change_state("walk")  # Transition T2
        elif self.runner.attack_zone.contains(self.runner.target):
            self.state_manager.change_state("prepare_attack")  # Transition T8

    def execute(self) -> None:
        self.runner.face_target()
        self.runner.velocity.x = self.runner.direction * self.runner.speed * 3


class PrepareAttackState(State):

    @property
    def runner(self):
        return self.state_manager.owner

    def update(self):
        if not self.runner.target:
            self.state_manager.change_state("walk")  # Transition T4
        elif not self.runner.continue_attack_zone.contains(self.runner.target):
            self.state_manager.change_state("run")  # Transition T3
        elif self.runner.is_facing(self.runner.target) and self.runner.on_ground and self.runner.stomp_cooldown <= 0:
            self.state_manager.change_state("stomp")  # Transition T6

    def execute(self) -> None:
        self.runner.face_target()
        self.runner.velocity.x = 0


class StompState(State):

    @property
    def runner(self):
        return self.state_manager.owner

    def update(self) -> None:
        if self.runner.on_ground and self.runner.velocity.y >= 0:  # Stomp action must be completed to exit this state
            if not self.runner.target:
                self.state_manager.change_state("walk")  # Transition T9
            elif not self.runner.attack_zone.contains(self.runner.target):
                self.state_manager.change_state("run")  # Transition 10
            else:
                self.state_manager.change_state("prepare_attack")  # Transition T7

    def enter(self):
        """
        Start stomping.
        """
        self.runner.velocity.y = -15
        self.runner.stomp_cooldown = 90

    def execute(self) -> None:
        pass

    def exit(self):
        for player in World.players:
            if self.runner.hit_zone.contains(player) and player.on_ground and player.can_take_damage:
                player.take_damage(1)  # Only vulnerable players take damage
                print(f"{player} got hit!")
        # TODO shake the camera (observer)
