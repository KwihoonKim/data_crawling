<Overview>

This repository provides a Python-based crawler for downloading reservoir water level data from the Korean Public Data Portal (공공데이터포털).
The script automatically retrieves historical reservoir water level records using the official Open API service and saves the data in a structured format (CSV).
This tool is designed for hydrological research, reservoir operation analysis, drought monitoring, and agricultural water resource management in Korea.

<Data Source>

Public Data Portal (공공데이터포털)
Reservoir Water Level Open API
Operated by relevant public institutions (e.g., K-water, Korea Rural Community Corporation)
Users must obtain their own service key from:
https://www.data.go.kr

Data usage must comply with the Public Data Portal policy.

<Features>

- Automatic API request using service key
- User-defined reservoir ID and date range
- Batch data collection
- Error handling for missing responses
- Export to CSV format
- Ready-to-use format for hydrological modeling

<Repository Structure>
├── reservoir_crawler.py
  
├── config.py

├── requirements.txt

├── example_output.csv

└── README.md
