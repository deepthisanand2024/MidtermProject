from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

class CommandHandler:
    def __init__(self):
        self.commands = {}
        self.plugin_commands = {}

    def register_command(self, command_name: str, command: Command):
        self.commands[command_name] = command

    #created for plugin commands
    def register_plugin_command(self, command_name: str, command: Command):
        self.plugin_commands[command_name] = command

    def execute_command(self, command:str, num1:float, num2:float):
        """Easier to ask for forgiveness than permission (EAFP) - Use when its going to most likely work"""
        try:
            #print(f'commands[command] {self.commands[command]}')
            return (self.commands[command].execute(num1, num2))
            
        except KeyError:
            print(f"No such command: {command}")
            logging.error(f"No such command: {command}")

    def execute_menu_command(self):
        """Easier to ask for forgiveness than permission (EAFP) - Use when its going to most likely work"""
        try:
            result, menu_op, menu_num = self.commands["menu"].execute(self.plugin_commands)
            return (result, menu_op, menu_num)
        except KeyError:
            print(f"No such command!")
            logging.error(f"No such command!")


import os
import pandas as pd, logging

class HistoryManager:
    
    def __init__(self, history_file='calculation_history.csv'):
        # Ensure the 'data' directory exists and is writable
        data_dir = './data'
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            logging.info(f"The directory '{data_dir}' is created")
            print(f"The directory '{data_dir}' is created")

        elif not os.access(data_dir, os.W_OK):
            logging.error(f"The directory '{data_dir}' is not writable.")
            print(f"The directory '{data_dir}' is not writable.")
        
        self.csv_file_path = os.path.join(data_dir, history_file)
        self.history = pd.DataFrame(columns=['Command', 'Arguments', 'Result'])
        self.history.to_csv(self.csv_file_path, index=False)

    def load_history(self):
        try:
            self.history = pd.read_csv(self.csv_file_path)
            print("History loaded successfully.")
            logging.info("History loaded successfully.")
            self.show_history()
        except FileNotFoundError:
            print("No history file found.")
            logging.error("No history file found.")

    def save_history(self):
        self.history.to_csv(self.csv_file_path, index=False)
        print("History saved successfully.")
        logging.info("History saved successfully.")

    def clear_history(self):
        self.history = pd.DataFrame(columns=['Command', 'Arguments', 'Result'])
        self.history.to_csv(self.csv_file_path, index=False)
        print("History cleared successfully.")
        logging.info("History cleared successfully.")

    def delete_history(self, index):
        if ((self.history.empty == False) and (index >= 0)):
            try:
                self.history.drop(index, inplace=True) 
                self.history.reset_index(drop=True, inplace=True)
                self.save_history()
                print(f"Record at index {index} deleted successfully.")
                logging.info(f"Record at index {index} deleted successfully.")  
                self.load_history()         
            except Exception as e:
                print(f"An error occurred while deleting the record: {e}")
                logging.error(f"An error occurred while deleting the record: {e}")
        
        elif (self.history.empty):
            logging.error(f"No calculation history available. Cannot delete records")
            print(f"No calculation history available. Cannot delete records")

        else: 
            logging.error("An error occurred while deleting the record!")
            print("An error occurred while deleting the record!")
            

    def show_history(self):
        if self.history.empty:
            print(f"No history to show.")
            logging.info(f"No history to show.")
        else:
            print(f'Calculation History Records: ')     
            logging.info(f'Calculation History Records: ')       
            for index, row in self.history.iterrows():                
                print(f"Record {index+1} :")
                logging.info(f"Record {index+1}: ")
                
                # Then, iterate through each field in the row to print and log
                for field in row.index:
                    field_info = f"    {field}: {row[field]}"
                    print(field_info)
                    logging.info(f"{field_info}")

    def add_to_history(self, command, args, result):
    
        new_record = pd.DataFrame({'Command': [command], 'Arguments': [args], 'Result': [result]})
        self.history = pd.concat([self.history, new_record], ignore_index=True)
        self.save_history()
