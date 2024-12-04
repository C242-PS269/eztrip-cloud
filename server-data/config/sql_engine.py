import os
import sqlalchemy as sa
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database credentials
Config = {
    'username': os.getenv('DB_USER'),   # MySQL username
    'password': os.getenv('DB_PASS'),   # MySQL password
    'database': os.getenv('DB_NAME'),   # Database name
    'host': os.getenv('DB_HOST'),       # Database host
    'port': os.getenv('DB_PORT')        # Database port
}

# Construct the SQLAlchemy connection string
engineURL = f"mysql+mysqlconnector://{Config['username']}:{Config['password']}@{Config['host']}:{Config['port']}/{Config['database']}"

# Create the SQLAlchemy engine
engine = sa.create_engine(engineURL)

# Test the connection to the MySQL database
def test_connection():
    try:
        with engine.connect() as connection:
            print("Connected to MySQL database successfully!")
    except Exception as e:
        print("Connection failed:", e)

# You can also export the engine to be used in other parts of the app
def get_engine():
    return engine
