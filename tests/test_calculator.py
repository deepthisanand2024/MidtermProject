# pylint: disable=unnecessary-dunder-call, pointless-string-statement,logging-fstring-interpolation, trailing-whitespace, invalid-name, missing-function-docstring, missing-module-docstring, disable=line-too-long,  unused-argument, redefined-outer-name

from io import StringIO
from contextlib import redirect_stdout
import logging
import logging.config
import os
import pandas as pd
import pytest
from calculator import App
from calculator.operations import HistoryManager


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

def test_configure_logging(monkeypatch):
    """Test logging configuration with different environment variables."""
    monkeypatch.setenv('LOG_LEVEL', 'INFO')
    monkeypatch.setenv('LOG_OUTPUT', 'file')
    monkeypatch.setenv('LOG_FILE', 'test_app.log')
    
    app = App()
    app.configure_logging()
    
    logger = logging.getLogger()
    assert logger.level == logging.INFO

@pytest.fixture
def history_manager():
    # Ensure the test does not interfere with the actual data
    return HistoryManager(history_file='test_calculation_history.csv')

def test_initialization(history_manager):
    """Test that the HistoryManager initializes correctly."""
    assert os.path.exists(history_manager.csv_file_path)
    assert os.path.isdir('./data')
    assert os.access('./data', os.W_OK)
    assert isinstance(history_manager.history, pd.DataFrame)
    assert set(history_manager.history.columns) == {'Command', 'Arguments', 'Result'}

def test_load_history(history_manager):
    """Test loading history."""
    history_manager.add_to_history('add', '1, 2', '3')
    history_manager.save_history()
    
    new_history_manager = HistoryManager(history_file='test_calculation_history.csv')
    with redirect_stdout(StringIO()) as output:
        new_history_manager.load_history()
    
    printed_output = output.getvalue().strip()
    assert "History loaded successfully." in printed_output

def test_save_history(history_manager):
    """Test saving history."""
    
    history_manager.add_to_history('add', '1, 2', '3')
    history_manager.save_history()
    
    loaded_history = pd.read_csv(history_manager.csv_file_path)
    assert len(loaded_history) == 1

def test_clear_history(history_manager):
    
    """Test clearing history."""
    history_manager.add_to_history('add', '1, 2', '3')
    history_manager.clear_history()
    
    assert history_manager.history.empty
    loaded_history = pd.read_csv(history_manager.csv_file_path)
    assert loaded_history.empty

def test_delete_history(history_manager):
    """Test deleting history."""
    
    history_manager.add_to_history('add', '1, 2', '3')
    history_manager.add_to_history('subtract', '5, 2', '3')
    history_manager.delete_history(0)
    
    assert len(history_manager.history) == 1
    assert history_manager.history.iloc[0]['Command'] == 'subtract'
    assert history_manager.history.iloc[0]['Arguments'] == '5, 2'
    assert str(history_manager.history.iloc[0]['Result']) == '3'

def test_show_history(history_manager):
    """Test showing history."""
    history_manager.add_to_history('add', '1, 2', '3')
    with redirect_stdout(StringIO()) as output:
        history_manager.show_history()
    
    printed_output = output.getvalue().strip()
    assert "Calculation History Records:" in printed_output
    assert "Record 1 :" in printed_output
    assert "Command: add" in printed_output
    assert "Arguments: 1, 2" in printed_output
    assert "Result: 3" in printed_output

def test_add_to_history(history_manager):
    """Test adding to history."""
    history_manager.add_to_history('add', '1, 2', '3')
    assert len(history_manager.history) == 1
    assert history_manager.history.iloc[0]['Command'] == 'add'
    assert history_manager.history.iloc[0]['Arguments'] == '1, 2'
    assert str(history_manager.history.iloc[0]['Result']) == '3'

    history_manager.add_to_history('subtract', '5, 2', '3')
    assert len(history_manager.history) == 2
    assert history_manager.history.iloc[1]['Command'] == 'subtract'
    assert history_manager.history.iloc[1]['Arguments'] == '5, 2'
    assert str(history_manager.history.iloc[1]['Result']) == '3'

def test_delete_history_negindex(monkeypatch):
    """Test the REPL 'delete history' command, including invalid indices."""
    inputs = iter(['delete history', '0', 'exit'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    app = App()
    app.history_manager.delete_history(-1)
    
    with redirect_stdout(StringIO()) as output:
        app.start()

    printed_output = output.getvalue().strip()
    print("printed_output : {printed_output}")
    assert "Index cannot be 0 or negative. Please enter valid index number." in printed_output


def test_delete_history_invalidindex(monkeypatch):
    """Test the REPL 'delete history' command, including invalid indices."""
    inputs = iter(['delete history', 'invalid', 'exit'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    app = App()
    app.history_manager.delete_history(-1)
    
    with redirect_stdout(StringIO()) as output:
        app.start()

    printed_output = output.getvalue().strip()
    print("printed_output : {printed_output}")
    assert "Invalid index. Please enter valid record number." in printed_output
    