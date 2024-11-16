import os
import dotenv

dotenv.load_dotenv()

DATABASE = {
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'username': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASS'),
    'database': os.getenv('DB_NAME')
}