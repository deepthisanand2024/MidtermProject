import os, sys, pkgutil
import importlib
from calculator.operations import CommandHandler
from calculator.operations import Command
from dotenv import load_dotenv
import logging
import logging.config

class App:
    def __init__(self): # Constructor
        os.makedirs('logs', exist_ok=True)
        self.configure_logging()
        load_dotenv()
        self.settings = self.load_environment_variables()
        self.settings.setdefault('ENVIRONMENT', 'PRODUCTION')
        self.command_handler = CommandHandler()

    def configure_logging(self):
        logging_conf_path = 'logging.conf'
        if os.path.exists(logging_conf_path):
            logging.config.fileConfig(logging_conf_path, disable_existing_loggers=False)
        else:
            logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.info("Logging configured.")

    def load_environment_variables(self):
        settings = {key: value for key, value in os.environ.items()}
        logging.info("Environment variables loaded.")
        return settings

    def get_environment_variable(self, env_var: str = 'ENVIRONMENT'):
        return self.settings.get(env_var, None)

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
                logging.info("Exiting the calculator. Goodbye!")
                sys.exit(0)
            
            elif command in ['add', 'subtract', 'multiply', 'divide']:
                # Input numbers from the user
                try:
                    num1 = float(input("Enter first number: "))
                    num2 = float(input("Enter second number: "))
                except ValueError:
                    logging.info("Invalid input. Please enter valid numbers.")
                    continue

                # Handle the command and get the result
                result =  self.command_handler.execute_command(command, num1, num2)

                # Display the result
                if result is not None:
                    logging.info(f"Result of {command} {num1} and {num2} is: {result}")
            else:
                # Handle unknown commands
                logging.info("Unknown command. Please enter a valid command.")
                sys.exit(0)
            