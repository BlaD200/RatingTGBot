import mysql.connector
from mysql.connector import MySQLConnection

from sql.config import *


def initialize_connection():
    return mysql.connector.connect(
        host=mysql_hostname,
        user=mysql_username,
        password=mysql_password,
        database=mysql_database
    )


def update_last_index(db: MySQLConnection, table_name: str, column_name: str):
    """
    Set the index of auto-increment column to the last used
    :param db:
    :param table_name: the name of the table to update the index in
    :param column_name: the name of the column to set the index for
    """
    cursor = db.cursor()
    s = "SELECT MAX(%s) FROM %s" % (column_name, table_name)
    cursor.execute(s)
    last_id = cursor.fetchall()
    # print(last_id, table_name)
    last_id = last_id[0][0]
    if last_id:
        last_id = int(last_id)
        cursor.execute("ALTER TABLE " + table_name + " auto_increment = %s", (last_id,))
    else:
        cursor.execute("ALTER TABLE " + table_name + " auto_increment = 0")
    db.commit()
