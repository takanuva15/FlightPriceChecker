
from src.flightscraper.GoogleFlightsScraper import GoogleFlightsScraper
from src.model.FlightData import FlightData
from src.model.FlightQuery import FlightQuery

# tmp = "https://www.google.com/flights#flt=LAX.LAS.2020-02-14;c:USD;e:1;md:360;dt:1800-2400;p:40000.2.USD;sd:1;t:f;tt:o"
# tmp = "https://www.google.com/flights#flt=ORD.BWI,/m/0dclg.2020-02-14;c:USD;e:1;md:360;dt:1800-2400;p:40000.2.USD;sd:1;t:f;tt:o"
# tmp = "https://www.google.com/flights#flt=ORD./m/0dclg.2020-02-14;c:USD;e:1;md:360;dt:1800-2400;p:40000.2.USD;sd:1;t:f;tt:o"
GOOGLE_FLIGHTS_URL = ("https://www.google.com/flights#"
                      "flt={dep_airport}.{arrival_airport}.{dep_date_as_yyyy_mm_dd};"
                      "c:USD;e:1;"
                      "md:{flight_duration_max_in_mins};"
                      "dt:{dep_time_min_as_dddd}-{dep_time_max_as_dddd};"
                      "p:{budget_max_in_cents}.2.USD;"
                      "sd:1;t:f;tt:o")


def get_matching_flights(flight_query: FlightQuery) -> list[FlightData]:
    url_to_check = GOOGLE_FLIGHTS_URL.format(
        dep_airport=flight_query.dep_airport,
        arrival_airport=flight_query.arrival_airport,
        dep_date_as_yyyy_mm_dd=flight_query.dep_date.strftime('%Y-%m-%d'),
        flight_duration_max_in_mins=flight_query.flight_duration_max*60,
        dep_time_min_as_dddd=flight_query.dep_time_min.strftime('%H%M'),
        dep_time_max_as_dddd=flight_query.dep_time_max.strftime('%H%M'),
        budget_max_in_cents=flight_query.budget_max*100
    )
    scraper = GoogleFlightsScraper(url_to_check)
    scraper.verify_flights_page_loaded()
    matching_flights = scraper.extract_matching_flights()
    scraper.close_browser()
    return matching_flights
