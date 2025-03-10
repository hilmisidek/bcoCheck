# bcoupdatecheck

## Description
This project provides a script to check updates on stock and price for BCO dropshippers. It offers an executable file (bco.exe) along with the necessary files to ensure it runs smoothly. Additionally, it includes the Python source code for those who prefer to use the script directly.

## Features
- **Check Updates:** Monitors stock and price updates for BCO products.
- **Executable File:** Easy to run executable (bco.exe) for quick setup.
- **Python Source Code:** Access to the script for customization and troubleshooting.

## Requirements
To use this script, you need the following:
- Python
- Selenium
- Pandas
- Openpyxl
- Chrome WebDriver (ensure it’s the latest version)

## Setup Instructions
1. Place all related files (bco.exe, init.xlsx, cred.txt, chromedriver.exe) in the same directory.
2. If the executable file fails to run, use the Python source code (`bco.py`) and follow the instructions below.
3. Edit `init.xlsx` to include each product URL.
4. Add your username and password to `cred.txt` (1st line: username, 2nd line: password).

## Troubleshooting
- If you encounter a “no such element” error during the login phase, comment out line 40 of the script.
- Tested and working on Windows 10 with Chrome 97 (error reported on Chrome version 96).
