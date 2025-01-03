from __future__ import annotations

from abc import ABC, abstractmethod


class StateManager:
    def __init__(self, master):
        self.master = master

    def change_state(self, new_state: State):
        self.master.state.exit()
        self.master.state = new_state
        self.master.state.enter()


class State(ABC):
    """
    Abstract base class for the runner's states in the finite state machine.
    """

    def __str__(self):
        return self.__class__.__name__

    @abstractmethod
    def update(self):
        ...

    def enter(self):
        pass

    @abstractmethod
    def execute(self) -> None:
        ...

    def exit(self):
        pass


class WalkState(State):

    def __init__(self, runner: "Runner"):
        self.runner = runner

    def update(self):
        # T1
        if self.runner.target and not self.runner.is_near(self.runner.target, self.runner.attack_range):
            self.runner.state_manager.change_state(self.runner.run_state)
        # T5
        if self.runner.target and self.runner.is_near(self.runner.target, self.runner.attack_range):
            self.runner.state_manager.change_state(self.runner.prepare_attack_state)

    def execute(self) -> None:
        self.runner.velocity.x = self.runner.direction * self.runner.speed
        old_x = self.runner.rect.x
        self.runner.rect.x += self.runner.velocity.x
        if self.runner.collision:  # Pre-check, if the runner would collide with something.
            self.runner.direction *= -1  # Turn around
            self.runner.velocity.x *= -1
        self.runner.rect.x = old_x  # Always reset the horizontal position, as the position update will be done later


class RunState(State):

    def __init__(self, runner: "Runner"):
        self.runner = runner

    def update(self):
        # T2
        if not self.runner.target:
            self.runner.state_manager.change_state(self.runner.walk_state)
        # T8
        if self.runner.target and self.runner.is_near(self.runner.target, self.runner.attack_range):
            self.runner.state_manager.change_state(self.runner.prepare_attack_state)

    def execute(self) -> None:
        self.runner.face_target(self.runner.target)
        self.runner.velocity.x = self.runner.direction * self.runner.speed * 3


class PrepareAttackState(State):

    def __init__(self, runner: "Runner"):
        self.runner = runner

    def update(self):
        # T4
        if not self.runner.target:
            self.runner.state_manager.change_state(self.runner.walk_state)
        # T3
        if self.runner.target and not self.runner.is_near(self.runner.target, self.runner.attack_range):
            self.runner.state_manager.change_state(self.runner.run_state)
        # T6
        if self.runner.target and self.runner.is_near(
                self.runner.target, self.runner.attack_range) and self.runner.is_facing(
            self.runner.target) and self.runner.on_ground and self.runner.stomp_cooldown <= 0:
            self.runner.state_manager.change_state(self.runner.stomp_state)

    def execute(self) -> None:
        self.runner.face_target(self.runner.target)
        self.runner.velocity.x = 0


class StompState(State):

    def __init__(self, runner: "Runner"):
        self.runner = runner

    def update(self):
        # T7
        if self.runner.on_ground and self.runner.velocity.y >= 0:
            self.runner.state_manager.change_state(self.runner.prepare_attack_state)

    def enter(self):
        """
        Start stomping.
        """
        self.runner.velocity.y = -12
        self.runner.stomp_cooldown = 90

    def execute(self) -> None:
        pass

    def exit(self):
        if self.runner.target and self.runner.is_near(
                self.runner.target, (self.runner.detect_range[0], 40)):
            if self.runner.target.can_take_damage and hasattr(self.runner.target, "take_damage"):
                self.runner.target.take_damage(1)  # Only vulnerable assets take damage
            print(f"{self.runner.target} got hit!")
        # TODO shake the camera (observer)
