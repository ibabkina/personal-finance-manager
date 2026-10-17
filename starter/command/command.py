# command.py

from abc import ABC, abstractmethod


class Command(ABC):
    """Command interface: an action that can be executed and undone."""

    @abstractmethod
    def execute(self):
        """Perform the action."""

    @abstractmethod
    def undo(self):
        """Reverse the action."""
