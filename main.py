#!/usr/local/bin/python3.9
# encoding: utf-8
'''
@author: takanuva15
'''
import sys

from src import config
from src.csvreader.FlightCriteriaReader import parse_flight_search_params
from src.flightscraper.FlightScraperController import get_matching_flights
from src.messaging.EmailHandler import send_email
from src.messaging.SmsHandler import send_text


def main():
    config.init()
    flights_to_check = parse_flight_search_params("sample_data_to_scrape.csv")
    for flight_query in flights_to_check:
        possible_flights = get_matching_flights(flight_query)
        if possible_flights:
            send_email(possible_flights)
            send_text(possible_flights)


if __name__ == "__main__":
    sys.exit(main())
