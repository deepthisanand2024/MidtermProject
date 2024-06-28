import sys, math
from calculator.operations import Command


class SinCommand(Command):
    def execute(self, menu_num):        
        print(f'inside execute for Sin command {math.sin(menu_num)}')
        return math.sin(menu_num)
