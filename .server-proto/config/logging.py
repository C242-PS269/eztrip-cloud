import logging

def setup_logging():
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("app.log"),  # Log to a file
            logging.StreamHandler()         # Log to the console
        ]
    )
    logger = logging.getLogger("FastAPI CRUD")
    return logger