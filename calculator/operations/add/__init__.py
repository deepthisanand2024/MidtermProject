import sys
from calculator.operations import Command
#from calculator.operations import add

class AddCommand(Command):
    def execute(self, num1:int, num2:int):
        #print(f'Performing Addition between {num1} and {num2}!')
        result  = add(num1, num2)   
        print(f'Result of addition: {result}')

def add(x, y):
    return x + y
