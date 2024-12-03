import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # MySQL configuration
    MYSQL_HOST = os.getenv('DB_HOST')
    MYSQL_USER = os.getenv('DB_USER')
    MYSQL_PASSWORD = os.getenv('DB_PASSWORD')
    MYSQL_DATABASE = os.getenv('DB_NAME')
