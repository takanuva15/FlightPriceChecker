import datetime
import logging as logger
import os
import re

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from . import WebDriverUtils
from ..model.FlightData import FlightData

'''
Created on Feb 8, 2020

@author: takanuva15
'''


class GoogleFlightsScraper(object):
    """
    Primary class to scrape Google Flights page and obtain data
    """
    def __init__(self, url: str):
        self.url = url

        script_dir = os.path.realpath('')
        driver_exe_path = os.path.join(script_dir, 'driver_exe', 'chromedriver.exe')
        self.driver = WebDriverUtils.start_new_chrome_browser(driver_exe_path)
        logger.info('Google Flights Scraper initialized. Browser started.')
        self.driver_wait = WebDriverWait(self.driver, 10)
        self.driver.get(url)
        logger.info('URL opened: %s', url)

    def verify_flights_page_loaded(self):
        self.driver_wait.until(EC.presence_of_element_located((By.XPATH, "//span[.='Flights']")))
        logger.info('Google Flights page loaded successfully')

    def extract_matching_flights(self) -> list[FlightData]:
        matching_flights: list[FlightData] = []
        date_raw = self.driver_wait.until(EC.presence_of_element_located(
            (By.XPATH, "//h1[.='Flight search']/../div[1]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/div/div[1]")
        )).get_attribute("data-value")
        logger.debug("Date found on flights page: %s", date_raw)

        # check flights under Best flights
        matching_flights.extend(self._extract_flights_under_header('Best flights', date_raw))
        # check flights under All flights
        matching_flights.extend(self._extract_flights_under_header('All flights', date_raw))

        return matching_flights

    def _extract_flights_under_header(self, header_label: str, dep_date_raw: str) -> list[FlightData]:
        matching_flights: list[FlightData] = []
        try:
            all_flights_header: WebElement = self.driver_wait.until(
                EC.presence_of_element_located((By.XPATH, f"//h3[.='{header_label}']"))
            )
            logger.debug(f"Found '{header_label}' label")
            all_flights_elements: list[WebElement] = all_flights_header.find_elements_by_xpath(
                "./../../../following-sibling::div//ol/li[@data-id]"
            )
            logger.info(f"Found %d flights listed under '{header_label}'", len(all_flights_elements))
            for flight in all_flights_elements:
                matching_flights.append(_generate_flight_data_from_flight_element(flight, dep_date_raw))
        except Exception as e:
            logger.info(f"Failed to find or extract flight data for the '{header_label}' label. %s", e)
        logger.debug(f'Matching flights for {header_label}: %s', matching_flights)
        return matching_flights

    def close_browser(self):
        self.driver.quit()
        logger.info('Closed the browser')


def _generate_flight_data_from_flight_element(flight_element: WebElement, dep_date_raw: str) -> FlightData:
    """
    Static function to generate the data needed for a FlightData object from an <li> in the list of flights on the
    Google Flights page
    """
    airline = flight_element.find_element_by_xpath("./div/div[1]/div/div[11]/span[6]").get_attribute("innerHTML")
    dep_airport = flight_element.find_element_by_xpath("./div/div[1]/div/div[5]").get_attribute("innerHTML")
    arrival_airport = flight_element.find_element_by_xpath("./div/div[1]/div/div[7]").get_attribute("innerHTML")
    dep_time_raw = flight_element.find_element_by_xpath("./div/div[1]/div/div[4]").get_attribute("innerHTML")
    arrival_time_raw = flight_element.find_element_by_xpath("./div/div[1]/div/div[6]").get_attribute("innerHTML")
    flight_duration_raw = flight_element.find_element_by_xpath("./div/div[1]/div/div[11]/span[3]").get_attribute(
        "innerHTML")
    flight_duration_hrs_raw = m.group(1) if (m := re.match(r'(\d+) hr', flight_duration_raw)) else 0
    flight_duration_mins_raw = m.group(1) if (m := re.search(r'(\d+) min', flight_duration_raw)) else 0
    price_raw: str = flight_element.find_element_by_xpath("./div/div[1]/div/div[9]/div[2]/span").get_attribute(
        "innerHTML")  # '$142'

    flight_data = FlightData(
        airline=airline,
        dep_date=datetime.datetime.strptime(dep_date_raw, '%Y-%m-%d'),
        dep_airport=dep_airport,
        arrival_airport=arrival_airport,
        dep_time=datetime.datetime.strptime(dep_time_raw, '%I:%M %p').time(),
        arrival_time=datetime.datetime.strptime(arrival_time_raw, '%I:%M %p').time(),
        flight_duration=datetime.timedelta(hours=int(flight_duration_hrs_raw), minutes=int(flight_duration_mins_raw)),
        stop_count=0,
        layover_time=datetime.timedelta(0),
        price=int(price_raw[1:])
    )
    logger.debug("Flight data extracted: %s", flight_data)
    return flight_data
