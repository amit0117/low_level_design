from typing import List, Dict, Any
from app.commands.base_command import Command
from app.models.enums import CommandStatus
import time


class CommandInvoker:
    """Invoker for executing commands with retry and rollback capabilities"""

    def __init__(self):
        self.executed_commands: List[Command] = []
        self.failed_commands: List[Command] = []

    def execute_command(self, command: Command) -> bool:
        """Execute a single command with retry logic"""
        print(f"Executing command: {command.__class__.__name__} - {command.get_command_id()}")

        while command.can_retry() or command.get_status() == CommandStatus.PENDING:
            try:
                if command.execute():
                    self.executed_commands.append(command)
                    print(f"Command executed successfully: {command.get_command_id()}")
                    return True
                else:
                    command.increment_retry()
                    if command.can_retry():
                        print(f"Command failed, retrying... ({command.retry_count}/{command.max_retries})")
                        time.sleep(1)  # Wait before retry
                    else:
                        self.failed_commands.append(command)
                        command.set_status(CommandStatus.FAILED)
                        print(f"Command failed permanently: {command.get_command_id()}")
                        return False
            except Exception as e:
                command.set_error(str(e))
                command.increment_retry()
                if not command.can_retry():
                    self.failed_commands.append(command)
                    print(f"Command failed with exception: {str(e)}")
                    return False

        return False

    def execute_commands(self, commands: List[Command]) -> Dict[str, Any]:
        """Execute multiple commands"""
        results = {"successful": [], "failed": [], "total": len(commands)}

        for command in commands:
            if self.execute_command(command):
                results["successful"].append(command.get_command_id())
            else:
                results["failed"].append(command.get_command_id())

        return results

    def rollback_last_command(self) -> bool:
        """Rollback the last executed command"""
        if not self.executed_commands:
            print("No commands to rollback")
            return False

        last_command = self.executed_commands.pop()
        print(f"Rolling back command: {last_command.__class__.__name__}")

        if last_command.undo():
            print("Rollback successful")
            return True
        else:
            print("Rollback failed")
            return False

    def rollback_all_commands(self) -> Dict[str, Any]:
        """Rollback all executed commands in reverse order"""
        rollback_results = {"successful": [], "failed": [], "total": len(self.executed_commands)}

        # Rollback in reverse order
        for command in reversed(self.executed_commands):
            if command.undo():
                rollback_results["successful"].append(command.get_command_id())
            else:
                rollback_results["failed"].append(command.get_command_id())

        self.executed_commands.clear()
        return rollback_results
