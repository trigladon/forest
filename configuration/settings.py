import os
from application.sites.helper import to_number

from jinja2 import (
    Environment,
    FileSystemLoader,
    select_autoescape
)


ALEGRO_URL = os.environ.get('ALEGRO_URL')
OLX_URL = os.environ.get('OLX_URL')

DB_NAME = os.environ.get('DB_NAME')

PRICE_FROM = to_number(os.environ.get('PRICE_FROM'))

EMAIL_FROM = os.environ.get('EMAIL_FROM')
EMAIL_TO = os.environ.get('EMAIL_TO')
EMAIL_URL = os.environ.get('EMAIL_URL')
EMAIL_PORT = to_number(os.environ.get('EMAIL_PORT'))
EMAIL_USERNAME = os.environ.get('EMAIL_USERNAME')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')

jinja_env = Environment(
    loader=FileSystemLoader('application/templates'),
    autoescape=select_autoescape(['html', 'xml'])
)


