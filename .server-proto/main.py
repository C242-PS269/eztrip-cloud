from fastapi import FastAPI
from config import database
import mysql.connector

db_config = database.DATABASE

app = FastAPI()

# Database Connection Function
def get_db_connection():
    global connection 
    connection = mysql.connector.connect(**db_config)
    return connection


@app.get("/")
def read_root():
    return {"Hello": "World"}