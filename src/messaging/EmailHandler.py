import logging as logger
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from prettytable import PrettyTable

from src import config
from src.model.FlightData import FlightData


def send_email(flight_data_list: list[FlightData]):
    if not flight_data_list:
        raise ValueError("flight_data_list should not be empty when emailing")

    message = MIMEMultipart('alternative')
    flight_data = flight_data_list[0]
    subject = "{dep_airport}→{arrival_airport} ({dep_date})".format(
        dep_airport=flight_data.dep_airport,
        arrival_airport=flight_data.arrival_airport,
        dep_date=flight_data.dep_date.strftime('%Y-%m-%d')
    )
    message['Subject'] = subject
    message['From'] = config.FROM_EMAIL
    message['To'] = config.TO_EMAIL

    build_email_body(message, flight_data_list)
    config.EMAIL_SERVER.sendmail(config.FROM_EMAIL, config.TO_EMAIL, message.as_string())
    logger.info("Email with subject '%s' sent successfully to %s", subject, config.TO_EMAIL)


def build_email_body(email_message: MIMEMultipart, flight_data_list: list[FlightData]):
    pt = PrettyTable()
    pt.field_names = ["Dep Date", "Dep Time", "Duration",
                      "Price", "From", "To",
                      "Arrival Time", "Stops", "Airline"]
    for flight_data in flight_data_list:
        pt.add_row([
            flight_data.dep_date.strftime('%Y-%m-%d'),
            flight_data.dep_time.strftime('%I:%M %p'),
            str(flight_data.flight_duration),
            '$' + str(flight_data.price),
            flight_data.dep_airport,
            flight_data.arrival_airport,
            flight_data.arrival_time.strftime('%I:%M %p'),
            flight_data.stop_count,
            flight_data.airline,
        ])

    email_message.attach(MIMEText("Matching flights:\n" + pt.get_string(), 'plain'))
    with open("src/messaging/matching_flights_email.html", "r") as f:
        html = f.read()
        html = html.replace("{table}", pt.get_html_string())
    email_message.attach(MIMEText(html, 'html'))
