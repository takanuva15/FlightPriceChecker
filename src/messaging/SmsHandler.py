import logging as logger

from src import config
from src.model.FlightData import FlightData


def send_text(flight_data_list: list[FlightData]):
    if not flight_data_list:
        raise ValueError("flight_data_list should not be empty when texting")

    flight_data = flight_data_list[0]
    msg_body = "{dep_airport}->{arrival_airport} ({dep_date}) Matching flights found. Please check your email.".format(
        dep_airport=flight_data.dep_airport,
        arrival_airport=flight_data.arrival_airport,
        dep_date=flight_data.dep_date.strftime('%Y-%m-%d')
    )
    config.EMAIL_SERVER.sendmail(config.FROM_EMAIL, config.TEXT_EMAIL, msg_body.strip())
    logger.info("SMS message '%s' sent successfully to %s", msg_body.strip(), config.TEXT_EMAIL)

