import logging
import os
from config.settings import ENV, LOG_FILE_PATH


def setup_logger():
    try:
        # Initialize logger
        logger = logging.getLogger()
        
        # Set logger level based on environment
        logger.setLevel(logging.DEBUG if ENV == 'DEBUG' else logging.INFO)
        
        # Define log format
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # Log to console
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # Remove existing log file if exists
        if os.path.exists(LOG_FILE_PATH):
            os.remove(LOG_FILE_PATH)
        
        # Log to file (optional)
        file_handler = logging.FileHandler(LOG_FILE_PATH)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        return logger

    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.error(f"Error setting up logger: {e}")
        raise  # Re-raise the exception after logging it