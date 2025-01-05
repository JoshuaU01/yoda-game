from __future__ import annotations

from abc import ABC, abstractmethod


class StateManager:
    def __init__(self, owner) -> None:
        self.owner = owner
        self.states = {}
        self.current_state = None

    def add_state(self, state: State, state_name: str, active: bool = False) -> None:
        if state_name in self.states:
            print(f"{self.states[state_name]} already exists in state manager.")
            return None
        self.states[state_name] = state  # Add state to the internal states dict
        state.attach_state_manager(self)
        if active:
            self.change_state(state)

    def change_state(self, new_state: State | str) -> None:
        # Convert state name to state object
        if isinstance(new_state, str):
            if new_state not in self.states:
                print(f"State {new_state} does not exist in state manager.")
                return None
            new_state = self.states[new_state]

        # Check if desired state has been added to state manager
        elif new_state not in self.states.values():
            print(f"{new_state} does not exist in state manager.")
            return None

        # Execute the state transition
        if self.current_state:
            self.current_state.exit()
        self.current_state = new_state
        self.current_state.enter()

    def update(self):
        if self.current_state is None:
            print("No state active. Initial state must be activated.")
            return None
        self.current_state.update()

    def execute(self):
        if self.current_state is None:
            print("No state active. Initial state must be activated.")
            return None
        self.current_state.execute()


class State(ABC):
    """
    Abstract base class for the states.
    The states are being centrally managed by the state manager.
    The states are represented as a finite state machine.
    """

    def __str__(self) -> str:
        return self.__class__.__name__

    def __init__(self) -> None:
        self.state_manager = None

    def attach_state_manager(self, state_manager: StateManager) -> None:
        self.state_manager = state_manager

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

    @property
    def runner(self):
        return self.state_manager.owner

    def update(self) -> None:
        if self.runner.target:
            if self.runner.is_near(self.runner.target, self.runner.attack_range):
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
        elif self.runner.is_near(self.runner.target, self.runner.attack_range):
            self.state_manager.change_state("prepare_attack")  # Transition T8

    def execute(self) -> None:
        self.runner.face_target(self.runner.target)
        self.runner.velocity.x = self.runner.direction * self.runner.speed * 3


class PrepareAttackState(State):

    @property
    def runner(self):
        return self.state_manager.owner

    def update(self):
        if not self.runner.target:
            self.state_manager.change_state("walk")  # Transition T4
        elif not self.runner.is_near(self.runner.target, self.runner.attack_range):
            self.state_manager.change_state("run")  # Transition T3
        elif self.runner.is_facing(self.runner.target) and self.runner.on_ground and self.runner.stomp_cooldown <= 0:
            self.state_manager.change_state("stomp")  # Transition T6

    def execute(self) -> None:
        self.runner.face_target(self.runner.target)
        self.runner.velocity.x = 0


class StompState(State):

    @property
    def runner(self):
        return self.state_manager.owner

    def update(self) -> None:
        if self.runner.on_ground and self.runner.velocity.y >= 0:  # Stomp action must be completed to exit this state
            if not self.runner.target:
                self.state_manager.change_state("walk")  # Transition T9
            elif not self.runner.is_near(self.runner.target, self.runner.attack_range):
                    self.state_manager.change_state("run")  # Transition 10
            else:
                self.state_manager.change_state("prepare_attack")  # Transition T7

    def enter(self):
        """
        Start stomping.
        """
        self.runner.velocity.y = -12
        self.runner.stomp_cooldown = 90

    def execute(self) -> None:
        pass

    def exit(self):
        if self.runner.target and self.runner.is_near(self.runner.target, (self.runner.detect_range[0], 40)):
            if self.runner.target.can_take_damage and hasattr(self.runner.target, "take_damage"):
                self.runner.target.take_damage(1)  # Only vulnerable assets take damage
            print(f"{self.runner.target} got hit!")
        # TODO shake the camera (observer)
