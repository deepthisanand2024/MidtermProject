# pylint: disable=unnecessary-dunder-call, trailing-whitespace, invalid-name, missing-function-docstring, missing-module-docstring, disable=line-too-long,  unused-argument, redefined-outer-name

from io import StringIO
from contextlib import redirect_stdout

#from calculator import App
from calculator.plugins.add import AddCommand
from calculator.plugins.subtract import SubtractCommand
from calculator.plugins.multiply import MultiplyCommand
from calculator.plugins.divide import DivideCommand

def test_add_command(capfd, monkeypatch):
    # Mock user input
    inputs = iter(['5', '10'])  # Simulate user entering '5' and '10'
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    command = AddCommand()
    with redirect_stdout(StringIO()) as output:
        command.execute(5, 10)
    
    printed_output = output.getvalue().strip()
    print('f {printed_output}')
    assert "Result of addition: 15" in printed_output

def test_subtract_command(capfd, monkeypatch):
    # Mock user input
    inputs = iter(['15', '10'])  # Simulate user entering '5' and '10'
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    command = SubtractCommand()
    with redirect_stdout(StringIO()) as output:
        command.execute(15, 10)
    printed_output = output.getvalue().strip()
    print('f {printed_output}')
    assert "Result of subtraction: 5" in printed_output

   
def test_multiply_command(capfd, monkeypatch):
    # Mock user input
    inputs = iter(['5', '10'])  # Simulate user entering '5' and '10'
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    command = MultiplyCommand()
    with redirect_stdout(StringIO()) as output:
        command.execute(5, 10)
    printed_output = output.getvalue().strip()
    print('f {printed_output}')
    assert "Result of multiplication: 50" in printed_output


def test_divide_command(capfd, monkeypatch):
    # Mock user input
    inputs = iter(['15', '5'])  # Simulate user entering '5' and '10'
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    command = DivideCommand()
    with redirect_stdout(StringIO()) as output:
        command.execute(15, 5)
    printed_output = output.getvalue().strip()
    print('f {printed_output}')
    assert "Result of division: 3" in printed_output

def test_dividebyzero_command(capfd, monkeypatch):
    # Mock user input
    inputs = iter(['15', '0'])  # Simulate user entering '5' and '10'
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    command = DivideCommand()
    with redirect_stdout(StringIO()) as output:
        command.execute(15, 0)
    printed_output = output.getvalue().strip()
    print('f {printed_output}')
    assert "Error: Division by zero" in printed_output
