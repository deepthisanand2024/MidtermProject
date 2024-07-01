import os
import pkgutil
import importlib
import sys

from calculator.operations import CommandHandler, Command
from calculator.operations.add import AddCommand
from calculator.operations.subtract import SubtractCommand
from calculator.operations.multiply import MultiplyCommand
from calculator.operations.divide import DivideCommand

from dotenv import load_dotenv
import logging
import logging.config

class App:
    def __init__(self): # Constructor
        os.makedirs('logs', exist_ok=True)
        #self.configure_logging()
        load_dotenv()
        self.settings = {}  # Initialize settings as an empty dictionary
        # Load all environment variables into settings
        for key, value in os.environ.items():
            self.settings[key] = value
        
        self.settings =  self.load_environment_variables()
        # Default to 'PRODUCTION' if 'ENVIRONMENT' not set
        self.settings.setdefault('ENVIRONMENT', 'DEV')    
        self.configure_logging()
        self.command_handler = CommandHandler()
       

    def configure_logging(self):
       
        try:
            log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
            log_output = os.getenv('LOG_OUTPUT', 'file').lower()
            log_format = format='%(asctime)s - %(levelname)s - %(message)s'
            logging.basicConfig(level = log_level, format =log_format)
            logger = logging.getLogger()
            logger.setLevel(log_level)
            
            if log_output == 'file':
                log_file = os.getenv('LOG_FILE', 'logs/app.log')
                file_handler = logging.FileHandler(log_file)
                file_handler.setFormatter(logging.Formatter(log_format))
                logger.addHandler(file_handler)
            else:
                raise ValueError(f"Unsupported LOG_OUTPUT value: {log_output}")
            logging.info("Logging configured.")
            
        except Exception as e:
                print(f"An error occurred while configuring logging: {e}")
                logging.error(f"An error occurred while configuring logging: {e}")


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
                    #print(f"Item : {item}")
                    try:
                        if issubclass(item, (Command)):  # Assuming a BaseCommand class exists
                            self.command_handler.register_plugin_command(plugin_name, item())
                            logging.info(f"Plugin {plugin_name} registered successfully.")
                            print(f"Plugin {plugin_name} registered successfully.")
                    except TypeError:
                        #logging.error(f"Error loading plugin {plugin_name}")
                        continue  # If item is not a class or unrelated class, just ignore
    def start(self):
        # Register commands here
        self.command_handler.register_command("add", AddCommand())
        self.command_handler.register_command("subtract", SubtractCommand())
        self.command_handler.register_command("multiply" , MultiplyCommand())
        self.command_handler.register_command("divide" , DivideCommand())
 
        while True:
            # Input command from the user  
            command = input("Enter command (choose one of the following options):\n"
            " - add\n"
            " - subtract\n"
            " - multiply\n"
            " - divide\n"
            " - exit (to quit)\n").strip().lower()
            
            if command == 'exit':
                logging.info("Exiting the calculator. Goodbye!")
                print("Exiting the calculator. Goodbye!")
                break
            
            elif command in ['add', 'subtract', 'multiply', 'divide']:
                # Input numbers from the user
                try:
                    num1 = float(input("Enter first number: "))
                    num2 = float(input("Enter second number: "))
                except ValueError:
                    logging.error("Invalid input. Please enter valid numbers.")
                    print("Invalid input. Please enter valid numbers.")
                    continue

                # Handle the command and get the result
                result =  self.command_handler.execute_command(command, num1, num2)
                # Display the result
                if result is not None:
                    logging.info(f"Result of {command} {num1} and {num2} is: {result}")
                    print(f"Result of {command} {num1} and {num2} is: {result}")
                                        
            else:
                # Handle unknown commands
                logging.error("Unknown command. Please enter a valid command.")
                print("Unknown command. Please enter a valid command.")
                break
            