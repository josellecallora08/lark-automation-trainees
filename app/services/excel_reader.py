import pandas as pd
import os
from typing import List, Dict, Any

class ExcelReader:
    def __init__(self, data_folder: str = "storage"):
        """
        Initialize the Excel Reader.
        
        Args:
            data_folder (str): Base folder for storing/reading Excel and CSV files
        """
        self.data_folder = data_folder
        os.makedirs(data_folder, exist_ok=True)

    def read_excel(self, file_path: str) -> pd.DataFrame:
        """
        Read an Excel file and return its contents as a pandas DataFrame.
        
        Args:
            file_path (str): Path to the Excel file (relative to data_folder)
            
        Returns:
            pd.DataFrame: The contents of the Excel file
        """
        full_path = os.path.join(self.data_folder, file_path)
        return pd.read_excel(full_path)

    def read_csv(self, file_path: str) -> pd.DataFrame:
        """
        Read a CSV file and return its contents as a pandas DataFrame.
        
        Args:
            file_path (str): Path to the CSV file (relative to data_folder)
            
        Returns:
            pd.DataFrame: The contents of the CSV file
        """
        full_path = os.path.join(self.data_folder, file_path)
        return pd.read_csv(full_path)

    def write_excel(self, df: pd.DataFrame, file_path: str) -> None:
        """
        Write a DataFrame to an Excel file.
        
        Args:
            df (pd.DataFrame): The DataFrame to write
            file_path (str): Path to write the Excel file to (relative to data_folder)
        """
        full_path = os.path.join(self.data_folder, file_path)
        df.to_excel(full_path, index=False)

    def write_csv(self, df: pd.DataFrame, file_path: str) -> None:
        """
        Write a DataFrame to a CSV file.
        
        Args:
            df (pd.DataFrame): The DataFrame to write
            file_path (str): Path to write the CSV file to (relative to data_folder)
        """
        full_path = os.path.join(self.data_folder, file_path)
        df.to_csv(full_path, index=False) 