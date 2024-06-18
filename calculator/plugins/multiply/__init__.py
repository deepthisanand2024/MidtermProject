import sys
from calculator.operations import Command
#from calculator.operations import multiply

class MultiplyCommand(Command):
    def execute(self, num1:int, num2:int):
        #print(f'Performing Multiplication!')
        result  =multiply(num1, num2)   
        print(f'Result of multiplication: {result}')

def multiply(x, y):
    return x * y
