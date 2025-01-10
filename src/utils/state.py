from __future__ import annotations

from abc import ABC, abstractmethod


class StateManager:
    """
    Class for managing states that are subclasses of State.
    The state manager can check and execute a transition between states
    and execute the current state.
    States must first be added to the state manager by using the add_state method.
    """

    def __init__(self, owner) -> None:
        """
        Creates an instance of this class.

        :param owner: The owner for which the state manager manages the states.
        """
        self.owner = owner
        self.states = {}
        self.current_state = None

    def add_state(self, state: State, state_name: str, active: bool = False) -> None:
        """
        Adds a state object to the internal dict of known states that can be used.

        :param state: The state object to be added.
        :param state_name: The name that the state can be accessed with.
        :param active: Whether the state shall be activated instantly (use for initial state).
        """
        if state_name in self.states:
            print(f"{self.states[state_name]} already exists in state manager.")
            return None
        self.states[state_name] = state  # Add state to the internal states dict
        state.attach_state_manager(self)
        if active:
            self.change_state(state)

    def change_state(self, new_state: State | str) -> None:
        """
        Executes a state transition. Does some pre-checks, calls the exit method of the current state (if exists)
        and the enter method of the new state. Sets the passed state as the current state.

        :param new_state: The state that the state manager shall switch to.
        Can be the state's name or the same object that has been added.
        """
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

    def update(self) -> None:
        """
        Calls the update method of the current state.
        """
        if self.current_state is None:
            print("No state active. Initial state must be activated.")
            return None
        self.current_state.update()

    def execute(self) -> None:
        """
        Calls the execute method of the current state.
        """
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
        """
        Overrides the default __str__ method to return the state class name.
        """
        return self.__class__.__name__

    def __init__(self) -> None:
        """
        Creates an instance of this class.
        """
        self.state_manager = None

    def attach_state_manager(self, state_manager: StateManager) -> None:
        """
        This method is called when the state is added to the state manager.

        :param state_manager: The state_manager that shall manage this state.
        """
        self.state_manager = state_manager

    @abstractmethod
    def update(self) -> None:
        """
        Abstract method that must be implemented by derived states.
        It handles the transitions between states.
        """
        ...

    def enter(self) -> None:
        """
        Optional method that can be implemented by derived states.
        It gets executed once while entering the state.
        """
        pass

    @abstractmethod
    def execute(self) -> None:
        """
        Abstract method that must be implemented by derived states.
        It gets executed repeatedly while this state is active.
        """
        ...

    def exit(self) -> None:
        """
        Optional method that can be implemented by derived states.
        It gets executed once while exiting the state.
        """
        pass
