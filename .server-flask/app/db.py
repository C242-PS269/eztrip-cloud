import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    _connection = None

    @classmethod
    def get_connection(cls):
        if cls._connection is None:
            cls._connection = mysql.connector.connect(
                host=f"{os.getenv("DB_HOST")}",
                user=f"{os.getenv("DB_USER")}",
                password=f"{os.getenv("DB_PASS")}",
                database=f"{os.getenv("DB_NAME")}"
            )
        return cls._connection

    @classmethod
    def close_connection(cls):
        if cls._connection is not None:
            cls._connection.close()
            cls._connection = None

def init_db():
    db = Database.get_connection()
    cursor = db.cursor()
    cursor.execute("SET time_zone = '+00:00';")
    db.commit()
