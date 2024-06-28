import sys, math
from calculator.operations import Command


class SqRtCommand(Command):
    def execute(self, menu_num):        
        print(f'inside execute for Sq Rt command {math.sqrt(menu_num)}')
        return math.sqrt(menu_num)
