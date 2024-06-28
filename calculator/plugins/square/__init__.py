import sys
from calculator.operations import Command


class SquareCommand(Command):
    def execute(self,menu_num):      
        print(f'inside execute for Sqaure command {(menu_num) ** 2}')
        return (menu_num) ** 2
        