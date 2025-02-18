import pandas as pd
import os
from typing import Dict, Optional, Tuple
import logging

# Set up logging
logging.basicConfig(
    filename='/workspaces/universal/CIHI_Knee_Hip_wait/code/error_log.txt',
    level=logging.INFO,  # Log level (INFO, WARNING, ERROR, etc.)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filemode='a'  # Append mode to avoid overwriting the log file
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

    def read_excel_file(self, filename: str, sheet_name: Optional[str] = None, header: Optional[int] = 0, usecols: Optional[range] = None) -> pd.DataFrame:
        """
        Safely read an Excel file with proper error handling.
        
        Args:
            filename (str): Name of the Excel file
            sheet_name (str, optional): Name of the sheet to read
            
        Returns:
            pd.DataFrame: DataFrame containing the Excel data
        """
        try:
            file_path = os.path.join(self.assets_path, filename)
            
            # Read with full options for proper data extraction
            if sheet_name:
                df = pd.read_excel(
                    file_path,
                    sheet_name=sheet_name,
                    header = header,
                    usecols= usecols,
                    engine='openpyxl',
                    na_values=['NA', 'N/A', ''],
                    keep_default_na=True
                )
            else:
                # Read all sheets if no sheet_name specified
                df = pd.read_excel(
                    file_path,
                    engine='openpyxl',
                    na_values=['NA', 'N/A', ''],
                    keep_default_na=True
                )
            
            logger.info(f"Successfully read {filename}")
            return df
            
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
            
            # Basic cleaning and preprocessing
            for procedure_name, df in procedures.items():
                procedures[procedure_name] = self._clean_wait_times_data(df)
            
            return procedures
            
        except Exception as e:
            logger.error(f"Error extracting wait times data: {str(e)}")
            raise

    def extract_hospital_spending(self) -> pd.DataFrame:
        """
        Extract hospital spending data.
        
        Returns:
            pd.DataFrame: Cleaned hospital spending data
        """
        try:
            spending_df = self.read_excel_file(self.hospital_spending_file)
            return self._clean_spending_data(spending_df)
            
        except Exception as e:
            logger.error(f"Error extracting hospital spending data: {str(e)}")
            raise

    def _clean_wait_times_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and preprocess wait times data.
        
        Args:
            df (pd.DataFrame): Raw wait times DataFrame
            
        Returns:
            pd.DataFrame: Cleaned DataFrame
        """
        cleaned_df = df.copy()
        
        # Remove any completely empty rows or columns
        cleaned_df.dropna(how='all', axis=0, inplace=True)
        cleaned_df.dropna(how='all', axis=1, inplace=True)
        
        # Convert wait time columns to numeric, coercing errors to NaN
        numeric_columns = cleaned_df.select_dtypes(include=['object']).columns
        for col in numeric_columns:
            cleaned_df[col] = pd.to_numeric(cleaned_df[col], errors='coerce')
        
        return cleaned_df

    def _clean_spending_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and preprocess hospital spending data.
        
        Args:
            df (pd.DataFrame): Raw hospital spending DataFrame
            
        Returns:
            pd.DataFrame: Cleaned DataFrame
        """
        cleaned_df = df.copy()
        
        # Remove any completely empty rows or columns
        cleaned_df.dropna(how='all', axis=0, inplace=True)
        cleaned_df.dropna(how='all', axis=1, inplace=True)
        
        # Convert spending columns to numeric, coercing errors to NaN
        numeric_columns = cleaned_df.select_dtypes(include=['object']).columns
        for col in numeric_columns:
            cleaned_df[col] = pd.to_numeric(cleaned_df[col], errors='coerce')
        
        return cleaned_df

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

# Usage example
if __name__ == "__main__":
    # Initialize extractor
    extractor = DataExtractor("assets")
    
    try:
        # Extract wait times data
        wait_times_data = extractor.extract_wait_times()
        print("Wait times data shape:", {k: v.shape for k, v in wait_times_data.items()})
        
        # Extract hospital spending data
        spending_data = extractor.extract_hospital_spending()
        print("Hospital spending data shape:", spending_data.shape)
        
        # Get merged data
        merged_data = extractor.get_merged_data()
        print("Merged data shape:", merged_data.shape)
        
    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}")