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
