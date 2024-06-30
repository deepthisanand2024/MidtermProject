import sys
from calculator.operations import Command
#from calculator.operations import subtract

class SubtractCommand(Command):
    def execute(self, num1:int, num2:int):
        #print(f'Performing Subtraction!')
        result  =subtract(num1, num2)   
        print(f'Result of subtraction: {result}')
        return result

def subtract(x, y):
    return x - y
