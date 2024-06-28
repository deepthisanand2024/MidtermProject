import sys, math
from calculator.operations import Command


class TanCommand(Command):
    def execute(self, menu_num):        
        print(f'inside execute for Tan command {math.tan(menu_num)}')
        return math.tan(menu_num)
