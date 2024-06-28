import sys
from calculator.operations import Command
import logging
import logging.config


class DivideCommand(Command):
    def execute(self, num1:int, num2:int):
        #print(f'Performing Division!')
        result  = divide(num1, num2) 
        if (isinstance(result, (float))) :
            logging.info(f'Result of division: {result}')
            print(f'Result of division: {result}')

def divide(x:int, y:int):
    if y != 0:
        return x / y
    else:
        logging.error("Error: Division by zero")
        return "Error: Division by zero"