from app import create_app
import dotenv
import os

dotenv.load_dotenv()

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host=os.getenv("SERVER_HOST"), port=os.getenv("SERVER_PORT"))
