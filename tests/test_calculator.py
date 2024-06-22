# pylint: disable=unnecessary-dunder-call, logging-fstring-interpolation, trailing-whitespace, invalid-name, missing-function-docstring, missing-module-docstring, disable=line-too-long,  unused-argument, redefined-outer-name

from io import StringIO
from contextlib import redirect_stdout
import logging
import logging.config
import pytest
from calculator import App


def test_app_start_exit_command(capfd, monkeypatch):
    """Test that the REPL exits correctly on 'exit' command."""
    # Simulate user entering 'exit'
    monkeypatch.setattr('builtins.input', lambda _: 'exit')
    
    # Redirect stdout to capture printed output
    with redirect_stdout(StringIO()) as output:
        App().start()

    # Read captured output from stdout
    printed_output = output.getvalue().strip()
    logging.info(f"Printed output: {printed_output}")
    # Assert that the exit message is printed
    assert "Exiting the calculator. Goodbye!" in printed_output

def test_app_unknown_command(capfd, monkeypatch):
    """Test that the REPL exits correctly on 'unknown' command."""
    # Simulate user entering 'unknown command'
    monkeypatch.setattr('builtins.input', lambda _: 'invalid')
    
    # Redirect stdout to capture printed output
    with redirect_stdout(StringIO()) as output:
        App().start()

    # Read captured output from stdout
    printed_output = output.getvalue().strip()
    logging.info('f {printed_output}')
    # Assert that the message is printed
    assert "Unknown command. Please enter a valid command." in printed_output

def test_app_invalidnumber_command(capfd, monkeypatch):
    """Test that the REPL exits correctly on 'unknown' command."""
    # Simulate user entering 'invalid numbers'
    inputs = iter(['add', '5', 'number' , 'exit']) 
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    # Redirect stdout to capture printed output
    with redirect_stdout(StringIO()) as output:
        App().start()

    # Read captured output from stdout
    printed_output = output.getvalue().strip()
    logging.info(f"Printed output: {printed_output}")
    #assert "Enter first number:" in printed_output
    #assert "Enter second number:" in printed_output
    assert "Invalid input. Please enter valid numbers.\nExiting the calculator. Goodbye!" in printed_output

    
@pytest.fixture
def app_instance():
    # Set up the App instance with mock environment variables
    return App()

def test_app_get_environment_variable(app_instance):
   # Test case 1: Check default environment setting
    assert app_instance.settings['ENVIRONMENT'] == 'DEV'

    # Test case 2: Mock setting 'ENVIRONMENT' to 'DEVELOPMENT'
    # Simulate loading environment variables
    app_instance.settings['ENVIRONMENT'] = 'TESTING'
    assert app_instance.settings['ENVIRONMENT'] == 'TESTING'

    # Test case 3: Mock setting 'ENVIRONMENT' to 'PRODUCTION'
    app_instance.settings['ENVIRONMENT'] = 'PRODUCTION'
    assert app_instance.settings['ENVIRONMENT'] == 'PRODUCTION'