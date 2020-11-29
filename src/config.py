import configparser
import logging as logger
import logging.config
import os
import smtplib

import yaml

# email/text credentials
USERNAME = None
PASSWORD = None
FROM_EMAIL = None
TO_EMAIL = None
TEXT_EMAIL = None

# other globals
EMAIL_SERVER = None


def init():
    """
    Set up logger and define global variables used for all files in the program
    """
    init_logging()
    logger.info('Initiating config')
    init_global_properties_from_config_ini()
    init_mail_server(USERNAME, PASSWORD)


def init_logging():
    os.makedirs('logs', exist_ok=True)  # logging config requires logs dir
    with open('logging-config.yml') as f:
        config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
        if __debug__:
            for handler in logging.getLogger().handlers:
                if type(handler) is logging.StreamHandler:
                    handler.setLevel(logging.DEBUG)
                    logger.debug('Console DEBUG logging enabled')
    logger.debug('Logging setup completed')


def init_global_properties_from_config_ini():
    config = configparser.ConfigParser()
    config.read('config.ini')

    section_name = 'local' if __debug__ else 'global'

    global USERNAME, PASSWORD, FROM_EMAIL, TO_EMAIL, TEXT_EMAIL
    USERNAME = config.get(section_name, 'USERNAME')
    PASSWORD = config.get(section_name, 'PASSWORD')
    FROM_EMAIL = config.get(section_name, 'FROM_EMAIL')
    TO_EMAIL = config.get(section_name, 'TO_EMAIL')
    TEXT_EMAIL = config.get(section_name, 'TEXT_EMAIL')
    logger.debug('Config global variables setup completed')


def init_mail_server(username, password) -> None:
    global EMAIL_SERVER
    EMAIL_SERVER = smtplib.SMTP('one.mxroute.com', 587)
    EMAIL_SERVER.ehlo()
    EMAIL_SERVER.starttls()
    EMAIL_SERVER.login(username, password)
    logger.info('Logged into mail server successfully')
