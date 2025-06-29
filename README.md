# Hikvision Branch Aggregator 

This Python tool connects to multiple Hikvision surveillance devices across different branches of a company, retrieves metadata, and normalizes the data into a unified CSV file.

## Features
- Secure API calls to remote Hikvision devices
- Parses metadata (ID, status, codec, resolution)
- Normalizes and translates camera names
- Outputs a unified dataset

## Setup
1. Add connection details to `branches_config.json`.
2. Install dependencies:
    ```
    pip install -r requirements.txt
    ```
3. Run the script:
    ```
    python main.py
    ```

*Note:* This project is a sanitized demonstration of an internal system under NDA. All sensitive data has been removed or obfuscated.
