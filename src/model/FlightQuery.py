'''
Created on Feb 9, 2020

@author: takanuva15
'''
from datetime import date, time


class FlightQuery:
    def __init__(self, dep_airport: str, arrival_airport: str, dep_date: date, dep_time_min: time, dep_time_max: time,
                 flight_duration_max: int, budget_max: int):
        self.dep_airport = dep_airport
        self.arrival_airport = arrival_airport
        self.dep_date = dep_date
        self.dep_time_min = dep_time_min
        self.dep_time_max = dep_time_max
        self.flight_duration_max = flight_duration_max
        self.budget_max = budget_max

    def __repr__(self):
        return str(self.__dict__)
