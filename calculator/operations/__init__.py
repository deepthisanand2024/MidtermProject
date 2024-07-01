from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

class CommandHandler:
    def __init__(self):
        self.commands = {}
        self.plugin_commands = {}

    def register_command(self, command_name: str, command: Command):
        self.commands[command_name] = command

    #created for plugin commands
    def register_plugin_command(self, command_name: str, command: Command):
        self.plugin_commands[command_name] = command

    def execute_command(self, command:str, num1:float, num2:float):
        """Easier to ask for forgiveness than permission (EAFP) - Use when its going to most likely work"""
        try:
            #print(f'commands[command] {self.commands[command]}')
            return (self.commands[command].execute(num1, num2))
            
        except KeyError:
            print(f"No such command: {command}")
            logging.error(f"No such command: {command}")

    def execute_menu_command(self):
        """Easier to ask for forgiveness than permission (EAFP) - Use when its going to most likely work"""
        try:
            result, menu_op, menu_num = self.commands["menu"].execute(self.plugin_commands)
            return (result, menu_op, menu_num)
        except KeyError:
            print(f"No such command!")
            logging.error(f"No such command!")


import os
import logging
