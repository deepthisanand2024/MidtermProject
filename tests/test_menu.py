# pylint: disable=unnecessary-dunder-call, trailing-newlines, pointless-string-statement,logging-fstring-interpolation, trailing-whitespace, invalid-name, missing-function-docstring, missing-module-docstring, disable=line-too-long,  unused-argument, redefined-outer-name

from io import StringIO
from contextlib import redirect_stdout
import pytest
from calculator.operations.menu import MenuCommand
from calculator.plugins.cos import CosCommand
from calculator.plugins.sin import SinCommand
from calculator.plugins.tan import TanCommand
from calculator.plugins.square import SquareCommand
from calculator.plugins.sqrt import SqRtCommand


@pytest.fixture
def menu_command():
    return MenuCommand()

def test_menu_display(menu_command, monkeypatch):
    """Test that the available menu commands are displayed correctly."""
    
    plugin_commands = {
        'cos': CosCommand(),
        'sin': SinCommand(),
        'sqrt': SqRtCommand(),
        'square': SquareCommand(),
        'tan': TanCommand()
    }

    inputs = iter(['exit'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    with redirect_stdout(StringIO()) as output:
        menu_command.execute(plugin_commands)
    
    printed_output = output.getvalue().strip()
    assert "Available Menu Commands:" in printed_output
    for command in plugin_commands:
        assert f" - {command}" in printed_output

def test_cos_command(capfd, monkeypatch):
    # Mock user input
    inputs = iter(['6'])  # Simulate user entering '5' and '10'
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    command = CosCommand()
    with redirect_stdout(StringIO()) as output:
        command.execute(6)
    
    printed_output = output.getvalue().strip()
    assert "0.960170286650366" in printed_output

def test_sin_command(capfd, monkeypatch):
    # Mock user input
    inputs = iter(['6'])  # Simulate user entering '5' and '10'
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    command = SinCommand()
    with redirect_stdout(StringIO()) as output:
        command.execute(6)
    
    printed_output = output.getvalue().strip()
    assert "-0.27941549819892586" in printed_output

def test_tan_command(capfd, monkeypatch):
    # Mock user input
    inputs = iter(['6'])  # Simulate user entering '5' and '10'
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    command = TanCommand()
    with redirect_stdout(StringIO()) as output:
        command.execute(6)
    
    printed_output = output.getvalue().strip()
    assert "-0.29100619138474915" in printed_output

def test_sqrt_command(capfd, monkeypatch):
    # Mock user input
    inputs = iter(['16'])  # Simulate user entering '5' and '10'
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    command = SqRtCommand()
    with redirect_stdout(StringIO()) as output:
        command.execute(16)
    
    printed_output = output.getvalue().strip()
    assert "4" in printed_output

def test_square_command(capfd, monkeypatch):
    # Mock user input
    inputs = iter(['4'])  # Simulate user entering '5' and '10'
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    command = SquareCommand()
    with redirect_stdout(StringIO()) as output:
        command.execute(4)
    
    printed_output = output.getvalue().strip()
    assert "16" in printed_output

def test_exit_menu_operation(menu_command, monkeypatch):
     
    plugin_commands = {
        'cos': CosCommand(),
        'sin': SinCommand(),
        'sqrt': SqRtCommand(),
        'square': SquareCommand(),
        'tan': TanCommand()
    }

    inputs = iter(['exit'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    with redirect_stdout(StringIO()) as output:
        menu_command.execute(plugin_commands)
    
    printed_output = output.getvalue().strip()
    assert "Back to Basic calculator operations!" in printed_output

def test_invalid_input(menu_command, monkeypatch):
     
    plugin_commands = {       
        'sqrt': SqRtCommand(),
    }

    inputs = iter(['sqrt', 'invalid_number', 'exit'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    with redirect_stdout(StringIO()) as output:
        menu_command.execute(plugin_commands)
    
    printed_output = output.getvalue().strip()
    assert "Available Menu Commands: \n - sqrt\nInvalid input. Please  provide valid number.\nBack to Basic calculator operations!" in printed_output

def test_invalid_menu_operation(menu_command, monkeypatch):
    """Test invalid menu operations."""
    
    plugin_commands = {
        'cos': CosCommand(),
    }

    inputs = iter(['invalid_command', 'exit'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    with redirect_stdout(StringIO()) as output:
        menu_command.execute(plugin_commands)
    
    printed_output = output.getvalue().strip()
    assert "No such plugin command: invalid_command" in printed_output

def test_execute_plugin(menu_command, monkeypatch):
        
    plugin_commands = {
        'cos': CosCommand(),
    }

    inputs = iter(['invalid_command', 'exit'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    with redirect_stdout(StringIO()) as output:
        menu_command.execute_plugin_command(plugin_commands, 'invalid_command', 2.0)
    
    printed_output = output.getvalue().strip()
    assert "No such plugin command: invalid_command" in printed_output
    