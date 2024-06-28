import sys
from calculator.operations import Command, CommandHandler
import logging
import logging.config


class MenuCommand(Command):
    
    def execute(self, plugin_commands):
        print(f"Available Menu Commands: ")
        for command in plugin_commands:
            print(f" - {command}")
        
        while True:
            try:
                menu_op = str(input("Choose menu operation (cos/sin/sqrt/square/tan) or exit: ").strip().lower())
                
                if menu_op == 'exit':
                    logging.info("Back to Basic calculator operations!")
                    print("Back to Basic calculator operations!")
                    break
                elif menu_op in plugin_commands:
                    menu_num = float(input("Enter a number for the selected operation: "))
                    #self.command_handler = CommandHandler()
                    result =  self.execute_plugin_command(plugin_commands, menu_op, menu_num)
                    # Display the result
                    if result is not None:
                        logging.info(f"Result of {menu_op} for {menu_num} is: {result:.4f}")
                        print(f"Result of {menu_op} for {menu_num} is: {result:.4f}")
                else:
                    raise KeyError

            except ValueError:
                logging.error("Invalid input. Please provide valid number.")
                print("Invalid input. Please  provide valid number.")
                continue
            except KeyError:
                logging.error(f"No such plugin command: {menu_op}")
                print(f"No such plugin command: {menu_op}")
                continue  
            

    def execute_plugin_command(self, plugin_commands, menu_op:str, menu_num: float):
        print(f'inside execute for menu ops')
        try:
            print(f'plugin_commands[menu_op] {plugin_commands[menu_op]}')
            return(plugin_commands[menu_op].execute(menu_num))
            
        except KeyError:
            logging.error(f"No such plugin command: {menu_op}")
            print(f"No such plugin command: {menu_op}")
