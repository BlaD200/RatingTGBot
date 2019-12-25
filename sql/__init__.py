import mysql.connector
from sql.config import *


def initialize_connection():
    return mysql.connector.connect(
        host=mysql_hostname,
        user=mysql_username,
        password=mysql_password,
        database=mysql_database
    )
