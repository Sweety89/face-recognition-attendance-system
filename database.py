import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    "host": "host",
    "port": port,
    "user": "user",
    "password": "password",
    "database": "database"
}

def get_connection():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as e:
        print("DB Connection Error:", e)
        return None
