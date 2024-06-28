import sys, math
from calculator.operations import Command


class CosCommand(Command):
    def execute(self, menu_num):        
        print(f'inside execute for Cos command {math.cos(menu_num)}')
        return math.cos(menu_num)
