import sqlite3

from . import settings


conn = sqlite3.connect(settings.DB_NAME)
cursor = conn.cursor()
