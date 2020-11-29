import datetime
import logging as logger
import time
from datetime import date

import pandas as pd

from src.model.FlightQuery import FlightQuery


def parse_flight_search_params(csv_file: str) -> list[FlightQuery]:
    """ Read csv file with the flights we want to look up.
    - Filters out flights that don't have 'active' search status in the 1st column
    """
    logger.info('Parsing flight queries from csv: %s', csv_file)
    flight_search_params = pd.read_csv(csv_file, sep=r'\s*,', engine='python')
    flight_search_params = flight_search_params[flight_search_params['Active'] == 'Y']
    flight_queries = []
    for row in flight_search_params.itertuples():
        generated_queries = _create_flight_queries_from_search_params(row)
        flight_queries.extend(generated_queries)
        logger.info('Generated %d flight queries from row %d successfully', len(generated_queries), row.Index + 1)
    logger.info('Generated %d queries total from csv successfully.', len(flight_queries))
    return flight_queries


def _create_flight_queries_from_search_params(flight_search_params) -> list[FlightQuery]:
    """ Given a row from the csv of the flight criteria, this will return a list of
    objects containing all the details the scraper needs to get flights matching
    the criteria
    :param flight_search_params:
    :return: list[FlightQuery]
    """
    num_weeks_to_check = flight_search_params.Num_Of_Weeks
    dep_day_as_int = time.strptime(flight_search_params.Dep_Day, "%a").tm_wday
    start_date_to_search_from = datetime.date.today() + datetime.timedelta(weeks=flight_search_params.Starting_Week)
    next_matching_dep_date = get_date_of_next_occurrence_of_day(start_date_to_search_from, dep_day_as_int)
    flight_query_list = []
    for i in range(num_weeks_to_check):
        flight_query_list.append(
            FlightQuery(
                dep_airport=flight_search_params.City_From,
                arrival_airport=flight_search_params.City_To,
                dep_date=next_matching_dep_date,
                dep_time_min=datetime.datetime.strptime(flight_search_params.Dep_Time_Min, '%I:%M %p').time(),
                dep_time_max=datetime.datetime.strptime(flight_search_params.Dep_Time_Max, '%I:%M %p').time(),
                flight_duration_max=flight_search_params.Max_Duration,
                budget_max=flight_search_params.Max_Budget
            )
        )
        logger.debug('Flight query generated: %s', flight_query_list[-1])
        next_matching_dep_date += datetime.timedelta(weeks=1)
    return flight_query_list


def get_date_of_next_occurrence_of_day(start_date: date, day_to_occur: int) -> date:
    return start_date + datetime.timedelta((day_to_occur - start_date.weekday()) % 7)
