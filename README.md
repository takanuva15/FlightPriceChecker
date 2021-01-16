# FlightPriceChecker
A simple Python program to check flight prices.

### Steps to execute:
- Put your flight criteria in the sample_data.csv file. (Currently the return columns are ignored. This will only calculate one-way trips)
- Put the email and text credentials you want to notify in config.ini
- Execute the program with `python -o main.py`

### Debugging:
You can enable 'debug mode' in the script by running without the -o flag. This will enable debug logging and show the browser during execution. 

### Handling booked flights:
For each row you add to the `data_to_scrape.csv`, the program will create a `.txt` file in the `booked_flights` directory under the repository directory.

Example: If you have a flight from JFK to LAX, it will create `JFK2LAX_booked_flights.txt`.

In that text file, add a single line with the date you have booked in `YYYY-MM-DD` format. The next time the script runs, it will not run any flight queries for the dates you have booked within the respective text file matching the travel path of the flight query.

### Requirements:
- Python 3.9+ 
- Must install all the relevant libraries used within the various `.py` files.
  - `pip3 install pandas pyvirtualdisplay selenium pyglet prettytable` 
