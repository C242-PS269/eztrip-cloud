# Import the required libraries
import mysql.connector # Used for MySQL-specific connections (via SQLAlchemy)
import sqlalchemy as sa
import os

from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

# Extract the database credentials from the environment variables
username = os.getenv('DB_USER')  # MySQL username
password = os.getenv('DB_PASS')     # MySQL password
database = os.getenv('DB_NAME')     # Database name
host = os.getenv('DB_HOST')         # Database host
port = os.getenv('DB_PORT')         # Database port

# Construct the SQLAlchemy connection string
engineURL = f"mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database}"

# Create the SQLAlchemy engine
engine = sa.create_engine(engineURL)

# Test the connection to the MySQL database
try:
    with engine.connect() as connection:
        print("Connected to MySQL database successfully!")
except Exception as e:
    # If there is an error, print the error message
    print("Connection failed:", e)