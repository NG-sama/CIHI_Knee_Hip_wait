import pandas as pd
import os
from typing import Dict, Optional, Union, Tuple
import logging
import sys
# Set up logging
# Create a memory handler that keeps only recent logs
memory_handler = logging.handlers.MemoryHandler(
    capacity=1000,  # Keep only last 1000 records
    flushLevel=logging.ERROR,  # Automatically flush on ERROR
    target=logging.StreamHandler(sys.stderr)  # Send to stderr for errors
)
# Configure logging to be minimal and memory-efficient
logging.basicConfig(
    level=logging.WARNING,  # Only log warnings and errors
    format='%(levelname)s - %(message)s',  # Simplified format
    handlers=[memory_handler]
)
logger = logging.getLogger(__name__)

class DataExtractor:
    def __init__(self, assets_path: str):
        """
        Initialize the DataExtractor with the path to the assets directory.
        
        Args:
            assets_path (str): Path to the directory containing the XLSX files
        """
        self.assets_path = assets_path
        self.wait_times_file = "wait-times-priority-procedures-in-canada-2024-data-tables-en.xlsx"
        self.hospital_spending_file = "hospital-spending-series-a-2005-2022-data-tables-en.xlsx"

    def read_excel_file(self, filename: str, sheet_name: Optional[Union[str,int]] = None, header: Optional[int] = 0, usecols: Optional[range] = None, skiprows: Optional[int] = 0, nrows: Optional[int] = None) -> Union[pd.DataFrame, Dict[str, pd.DataFrame]]:
        """
            Read an Excel file and return the data from a specific sheet or all sheets.
            
            Args:
                filename (str): Path to the Excel file.
                sheet_name (str or int, optional): Name or index of the sheet to read. If not specified, all sheets are read.
                header (int, optional): Row number to use as column names (default is 0, the first row).
                usecols (range, optional): Specifies which columns to read from the file.
                skiprows (int,optional): Number of rows to skip at the start (default is 0).
                nrows (int, optional): Number of rows to read (default is None, which reads all rows).
            Returns:
                Union[pd.DataFrame, Dict[str, pd.DataFrame]]:
                - If a specific sheet is requested, returns a single `DataFrame` for that sheet.
                - If no `sheet_name` is provided, returns a dictionary where the keys are sheet names and the values are `DataFrame` objects for each sheet.
            """
        try:
            file_path = os.path.join(self.assets_path, filename)
            
            # Read with full options for proper data extraction
            if isinstance(sheet_name,str):
                df = pd.read_excel(
                    file_path,
                    sheet_name=sheet_name,
                    header = header,
                    usecols= usecols,
                    engine='openpyxl',
                    na_values=['NA', 'N/A', ''],
                    keep_default_na=True
                )
                logger.info(f"Successfully read {filename}")
                return df
            else:
                # Read all sheets if no sheet_name specified
                name_of_sheet = pd.ExcelFile(file_path).sheet_names
                df = pd.read_excel(
                    file_path,
                    sheet_name=sheet_name,
                    header = header,
                    usecols= usecols,
                    engine='openpyxl',
                    skiprows=skiprows, 
                    nrows=nrows,
                    na_values=['NA', 'N/A', ''],
                    keep_default_na=True
                )
                logger.info(f"Successfully read sheet {name_of_sheet[sheet_name]} from {filename}")
                return df, name_of_sheet[sheet_name]
            
        except FileNotFoundError:
            logger.error(f"File not found: {filename}")
            raise
        except Exception as e:
            logger.error(f"Error reading {filename}: {str(e)}")
            raise

    def extract_wait_times(self) -> Dict[str, pd.DataFrame]:
        """
        Extract wait times data for different procedures.
        
        Returns:
            Dict[str, pd.DataFrame]: Dictionary containing DataFrames for different procedures
        """
        try:
            wait_times_df = self.read_excel_file(self.wait_times_file, "Wait times 2008 to 2023", header = 2, usecols=range(8))
            
            # Extract specific procedures
            procedures = {
                'hip_replacement': wait_times_df[wait_times_df['Indicator'] == 'Hip Replacement'],
                'knee_replacement': wait_times_df[wait_times_df['Indicator'] == 'Knee Replacement']
            }
 
            return procedures
            
        except Exception as e:
            logger.error(f"Error extracting wait times data: {str(e)}")
            raise

    def extract_hospital_spending(self) -> Dict[str, pd.DataFrame]:
        """
        Extract hospital spending data.
        
        Returns:
            Dict[str, pd.DataFrame]: Dictionary with sheet names as keys and corresponding DataFrames as values.        """
        try:
            province_spending = {}
            for i in range(2,14):
                spending_df, name_sheet = self.read_excel_file(self.hospital_spending_file, sheet_name= i,header= 4, nrows= 18)
                province_spending[name_sheet] = spending_df
        
            return province_spending
            
        except Exception as e:
            logger.error(f"Error extracting hospital spending data: {str(e)}")
            raise

    def get_merged_data(self) -> pd.DataFrame:
        """
        Merge wait times and hospital spending data.
        
        Returns:
            pd.DataFrame: Merged DataFrame containing both wait times and spending data
        """
        try:
            wait_times = self.extract_wait_times()
            spending = self.extract_hospital_spending()
            
            # Merge logic here - will need to be customized based on actual data structure
            # This is a placeholder for the actual merge logic
            merged_df = pd.merge(
                wait_times['hip_replacement'],
                spending,
                on=['Province', 'Year'],
                how='inner'
            )
            
            return merged_df
            
        except Exception as e:
            logger.error(f"Error merging data: {str(e)}")
            raise