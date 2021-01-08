import datetime
import os
import logging as logger
import pandas as pd

from datetime import date
from src.model.FlightQuery import FlightQuery


class BookedFlightsHandler:
    BOOKED_FLIGHTS_DIR = 'booked_flights'
    BOOKED_FLIGHT_FILENAME = '{travel_path}_booked_flights.txt'

    """
    Takes in all list of flight queries to process. Based on the flights given,
    it will generate (or read) the appropriate booked text files to see
    whether there are any existing booked flight dates that should be ignored
    before executing the existing flight queries
    """
    def __init__(self, flight_queries_to_filter: list[FlightQuery]):
        self.booked_flights: dict[str, [date]] = {}
        self.flight_queries = flight_queries_to_filter
        df_flight_queries = pd.DataFrame([{**vars(s), 'ref': s} for s in self.flight_queries])

        os.makedirs(self.BOOKED_FLIGHTS_DIR, exist_ok=True)
        df_unique_travel_paths = df_flight_queries.drop_duplicates(subset=['dep_airport', 'arrival_airport'])
        df_unique_travel_paths.apply(lambda x: _generate_booked_flights_file_if_not_exist(x['dep_airport'], x['arrival_airport']), axis='columns')

    def read_booked_flight_dates_from_files(self):
        for entry in os.scandir(self.BOOKED_FLIGHTS_DIR):  # type: os.DirEntry
            with open(entry.path) as f:
                booked_date_list = [datetime.datetime.strptime(iso_date.strip(), '%Y-%m-%d').date() for iso_date in f]
            self.booked_flights[entry.name[:7]] = booked_date_list
        logger.debug('Booked flight dates found: %s', self.booked_flights)
        return self

    def remove_passed_dates_from_files(self):
        for travel_path, booked_dates in self.booked_flights.items():
            filtered_dates: list[date] = []
            for booked_date in booked_dates:
                if booked_date < datetime.date.today():
                    logger.info("Deleting past date %s found in %s...", booked_date,
                                BookedFlightsHandler.BOOKED_FLIGHT_FILENAME.format(travel_path=travel_path))
                else:
                    filtered_dates.append(booked_date)
            self.booked_flights[travel_path] = filtered_dates
            booked_flights_filename = BookedFlightsHandler.BOOKED_FLIGHT_FILENAME.format(travel_path=travel_path)
            booked_flights_file_fullpath = os.path.join(BookedFlightsHandler.BOOKED_FLIGHTS_DIR, booked_flights_filename)
            with open(booked_flights_file_fullpath, 'w') as f:
                f.writelines(f"{booked_date}\n" for booked_date in filtered_dates)
        return self

    def remove_booked_flight_dates_from_flight_queries(self):
        flight_queries_filtered: list[FlightQuery] = []
        for flight_query in self.flight_queries:
            if flight_query.travel_path in self.booked_flights and \
                    flight_query.dep_date in self.booked_flights[flight_query.travel_path]:
                logger.info("Found a booked flight for %s on %s. Removing from flight queries list...",
                            flight_query.travel_path, flight_query.dep_date_fo_str)
            else:
                flight_queries_filtered.append(flight_query)
        logger.info("Updated queries list now has %d queries after filtering.", len(flight_queries_filtered))
        return flight_queries_filtered


def _generate_booked_flights_file_if_not_exist(dep_airport, arrival_airport):
    travel_path = dep_airport + '2' + arrival_airport
    booked_flights_filename = BookedFlightsHandler.BOOKED_FLIGHT_FILENAME.format(travel_path=travel_path)
    booked_flights_file_fullpath = os.path.join(BookedFlightsHandler.BOOKED_FLIGHTS_DIR, booked_flights_filename)
    if not os.path.exists(booked_flights_file_fullpath):
        logger.info('No booked_flights file detected for flight query %s. Creating %s...',
                    travel_path, booked_flights_filename)
        open(booked_flights_file_fullpath, 'w').close()
