import sys
from calculator.operations import Command
#from calculator.operations import divide


class DivideCommand(Command):
    def execute(self, num1:int, num2:int):
        #print(f'Performing Division!')
        result  = divide(num1, num2)   
        print(f'Result of division: {result}')

def divide(x:int, y:int):
    if y != 0:
        return x / y
    else:
        return "Error: Division by zero"