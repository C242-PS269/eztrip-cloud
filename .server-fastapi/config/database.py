import os
import dotenv
import mysql.connector

dotenv.load_dotenv()

DATABASE = {
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'username': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASS'),
    'database': os.getenv('DB_NAME')
}

conn = None

async def connect_db():
    """Connect to the database."""
    global conn
    try:
        conn = mysql.connector.connect(**DATABASE)
        return conn
    except Exception as e:
        raise Exception(f"Database connection failed: {e}")

async def close_db():
    """Close the database connection."""
    if conn and conn.is_connected():
        conn.close()
