# command_manager.py


class CommandManager:
    """Invoker: runs commands and remembers them so the last one can be undone."""

    def __init__(self):
        self._history = []

    def execute_command(self, command):
        """Execute a command and add it to the history."""
        command.execute()
        self._history.append(command)

    def undo_last(self):
        """Undo the most recent command. Returns True if something was undone, False if not."""
        if not self._history:
            return False
        command = self._history.pop()
        command.undo()
        return True
