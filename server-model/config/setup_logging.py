import logging

# Function to configure logging
def log():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            # Log to a file
            logging.FileHandler("app.log"),
            # Log to console
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger("EzTrip ML-Model Server")
    return logger