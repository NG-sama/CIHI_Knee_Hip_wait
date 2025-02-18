import logging
import time
from extract_data import DataExtractor

# Configure logging
logging.basicConfig(
    filename='/workspaces/universal/CIHI_Knee_Hip_wait/code/error_log.txt',
    level=logging.INFO,  # You can change this to logging.DEBUG for more detailed output
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='a'  # 'a' for append mode, so logs don't overwrite previous ones
)

# Get current timestamp
timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

# Log the start of the run with timestamp
logging.info(f"Run started at: {timestamp}")

# Initialize the extractor
try:
    extractor = DataExtractor("/workspaces/universal/CIHI_Knee_Hip_wait/assets")
    logging.info("DataExtractor initialized successfully.")
except Exception as e:
    logging.error(f"Error initializing DataExtractor: {e}")
    raise

# Try extracting wait times data and log any errors
try:
    wait_times = extractor.extract_wait_times()
    logging.info(f"Wait times data extracted successfully: {wait_times}")
except Exception as e:
    logging.error(f"Error extracting wait times: {e}")

# # Try extracting hospital spending data and log any errors
# try:
#     spending = extractor.extract_hospital_spending()
#     logging.info(f"Hospital spending data extracted successfully: {spending}")
# except Exception as e:
#     logging.error(f"Error extracting hospital spending: {e}")

# # Try getting merged data for analysis and log any errors
# try:
#     merged_data = extractor.get_merged_data()
#     logging.info(f"Merged data extracted successfully: {merged_data}")
# except Exception as e:
#     logging.error(f"Error extracting merged data: {e}")
