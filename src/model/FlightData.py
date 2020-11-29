'''
Created on Feb 9, 2020

@author: takanuva15
'''
from datetime import date, time, timedelta


class FlightData:
    def __init__(self, airline: str, dep_date: date, dep_airport: str, arrival_airport: str,
                 dep_time: time, arrival_time: time, flight_duration: timedelta, stop_count: int,
                 layover_time: timedelta, price: int):
        self.airline = airline
        self.dep_date = dep_date
        self.dep_airport = dep_airport
        self.arrival_airport = arrival_airport
        self.dep_time = dep_time
        self.arrival_time = arrival_time
        self.flight_duration = flight_duration
        self.stop_count = stop_count
        self.layover_time = layover_time
        self.price = price

    def __repr__(self):
        return str(self.__dict__)
