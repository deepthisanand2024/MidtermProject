from calculator.operations import CommandHandler
from calculator.operations.add import AddCommand
from calculator.operations.subtract import SubtractCommand
from calculator.operations.multiply import MultiplyCommand
from calculator.operations.divide import DivideCommand

class App:
    def __init__(self): # Constructor
        self.command_handler = CommandHandler()


    def start(self):
        # Register commands here
        self.command_handler.register_command("add", AddCommand())
        self.command_handler.register_command("subtract", SubtractCommand())
        self.command_handler.register_command("multiply" , MultiplyCommand())
        self.command_handler.register_command("divide" , DivideCommand())
        
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
                #continue
                break


