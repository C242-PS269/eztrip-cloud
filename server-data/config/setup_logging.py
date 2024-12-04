# Import required library
import logging

# Function to configure logging
def log():
    """
    Configures logging for the application.

    This function sets up logging to both a file and the console with the following properties:
    - Logs messages at the INFO level or higher.
    - The log messages include the timestamp, logger name, log level, and message content.
    - Logs are saved in a file named "app.log" in the application's directory.
    - Logs are also displayed on the console (stdout).

    Returns:
        logger (logging.Logger): Configured logger instance for the application.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            # Log to a file named 'app.log'
            logging.FileHandler("app.log"),
            # Log to the console (stdout)
            logging.StreamHandler()
        ]
    )

    # Create and return a logger instance with the name 'EzTrip Data Server'
    logger = logging.getLogger("EzTrip Data Server")
    return logger