import settings
import environment

import mysql.connector.pooling as pooling

pool = pooling.MySQLConnectionPool(**settings.app_settings["db_connection"])

def get_connection():
    if (pool):
        return pool.get_connection()

