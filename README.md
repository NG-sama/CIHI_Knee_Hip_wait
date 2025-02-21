# CIHI Knee and Hip Wait Times Analysis

## Overview
This project analyzes wait times for knee and hip surgeries across different regions and provinces in Canada, correlating them with provincial healthcare spending. The analysis is based on data provided by the Canadian Institute for Health Information (CIHI).

## Features
- Analysis of knee and hip surgery wait times across Canadian provinces
- Correlation analysis between hospital spending and wait times
- Provincial healthcare spending analysis
- Data extraction and processing utilities

## Project Structure
```
/CIHI_Knee_Hip_wait
├── /assets/                 # Excel data files
├── /code/                   # Source code
│   ├── __pycache__/        # Python cache directory
│   ├── extract_data.py     # Data extraction utilities
│   ├── main.py             # Main application entry point
│   ├── visualize_data.py   # Visualization functions
│   └── error_log.txt       # Application logs
├── /tests/                 # Test files
├── .gitignore
├── LICENSE.md              
├── README.md               
└── requirements.txt        # Project dependencies
```

## Prerequisites
- Python 3.8+
- pip package manager

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/CIHI_Knee_Hip_wait.git
cd CIHI_Knee_Hip_wait
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Data Files
Place the following Excel files in the `/assets` directory:
- `wait-times-priority-procedures-in-canada-2024-data-tables-en.xlsx`
- `hospital-spending-series-a-2005-2022-data-tables-en.xlsx`

## Usage

The project provides utilities for:
1. Extracting wait times and hospital spending data
2. Processing and analyzing the data
3. Generating visualizations and insights

Example usage:
```python
from extract_data import DataExtractor

# Initialize the extractor
extractor = DataExtractor("path/to/assets")

# Extract wait times data
wait_times = extractor.extract_wait_times()

# Extract hospital spending data
spending = extractor.extract_hospital_spending()
```

## Data Processing

The project handles data processing in several stages:

1. **Data Extraction**: Raw data is extracted from Excel files using the `DataExtractor` class
2. **Analysis**: Statistical analysis and correlation studies
3. **Visualization**: Generation of charts and visualizations

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License and Acknowledgment
This project uses data from the Canadian Institute for Health Information (CIHI) and is subject to CIHI's Terms of Use. The data is provided for educational, non-commercial research, internal reference, and private study purposes only.

All data and materials from CIHI must be properly credited to CIHI as the source. Commercial use of CIHI materials is prohibited without explicit written permission from CIHI.

For full license terms and conditions, please see the [LICENSE](LICENSE.md) file.

For questions regarding CIHI data usage or to request permission for commercial use, contact CIHI at copyright@cihi.ca.