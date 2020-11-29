# FlightPriceChecker
A simple Python program to check flight prices.

## Steps to execute:
- Put your flight criteria in the sample_data.csv file. (Currently the return columns are ignored. This will only calculate one-way trips)
- Put the email and text credentials you want to notify in config.ini
- Execute the program with `python -o main.py`

## Debugging:
You can enable 'debug mode' in the script by running without the -o flag. This will enable debug logging and show the browser during execution. 

### Requirements:
- Python 3.9+ 
- Must install all the relevant libraries used within the various `.py` files.
