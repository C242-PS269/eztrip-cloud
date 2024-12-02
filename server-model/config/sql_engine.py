import mysql.connector
import sqlalchemy as sa

username = 'GCP-SQL-ISNTANCE-USER'
password = 'GCP-SQL-ISNTANCE-PASSWORD'
database = 'DB-NAME'
host = 'GCP-SQL-INSTANCE'
port = '3306'

# Create the connection string
engineURL = f"mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database}"
# Create the engine
engine = sa.create_engine(engineURL)

# Test the connection
try:
    with engine.connect() as connection:
        print("Connected to MySQL database successfully!")
except Exception as e:
    print("Connection failed:", e)