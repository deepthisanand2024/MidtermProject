import pkgutil
import importlib
from calculator.operations import CommandHandler
from calculator.operations import Command

class App:
    def __init__(self): # Constructor
        self.command_handler = CommandHandler()

    def load_plugins(self):
        # Dynamically load all plugins in the plugins directory
        plugins_package = 'calculator.plugins'
        for _, plugin_name, is_pkg in pkgutil.iter_modules([plugins_package.replace('.', '/')]):
            if is_pkg:  # Ensure it's a package
                plugin_module = importlib.import_module(f'{plugins_package}.{plugin_name}')
                for item_name in dir(plugin_module):
                    item = getattr(plugin_module, item_name)
                    try:
                        if issubclass(item, (Command)):  # Assuming a BaseCommand class exists
                            self.command_handler.register_command(plugin_name, item())
                    except TypeError:
                        continue  # If item is not a class or unrelated class, just ignore
    def start(self):
        # Register commands here
        self.load_plugins()
        while True:
            # Input command from the user
            command = input("Enter command (add/subtract/multiply/divide, 'exit' to quit): ").strip().lower()
            if command == 'exit':
                print("Exiting the calculator. Goodbye!")
                break
            
            elif command in ['add', 'subtract', 'multiply', 'divide']:
                # Input numbers from the user
                try:
                    num1 = float(input("Enter first number: "))
                    num2 = float(input("Enter second number: "))
                except ValueError:
                    print("Invalid input. Please enter valid numbers.")
                    continue

                # Handle the command and get the result
                result =  self.command_handler.execute_command(command, num1, num2)

                # Display the result
                if result is not None:
                    print(f"Result of {command} {num1} and {num2} is: {result}")
            else:
                # Handle unknown commands
                print("Unknown command. Please enter a valid command.")
                break
            