from abc import ABC, abstractmethod


class State(ABC):
    """
    Abstract base class for the runner's states in the finite state machine.
    """

    def __str__(self):
        return self.__class__.__name__

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

    def execute(self) -> None:
        self.runner.face_target(self.runner.target)
        self.runner.velocity.x = self.runner.direction * self.runner.speed * 3


class PrepareAttackState(State):

    def __init__(self, runner: "Runner"):
        self.runner = runner

    def execute(self) -> None:
        self.runner.face_target(self.runner.target)
        self.runner.velocity.x = 0


class StompState(State):

    def __init__(self, runner: "Runner"):
        self.runner = runner

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
