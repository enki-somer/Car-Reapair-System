import os
import logging
from logging.handlers import RotatingFileHandler
import sys
import appdirs

def setup_logging():
    # Create logger
    logger = logging.getLogger('mahalli')
    logger.setLevel(logging.INFO)

    try:
        # Use appdirs to get the appropriate user data directory
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            log_dir = os.path.join(appdirs.user_log_dir('mahalli', appauthor=False))
        else:
            # Running from source
            log_dir = 'logs'

        # Create logs directory if it doesn't exist
        os.makedirs(log_dir, exist_ok=True)

        # File handler for all logs
        file_handler = RotatingFileHandler(
            os.path.join(log_dir, 'mahalli.log'),
            maxBytes=5*1024*1024,  # 5MB
            backupCount=5
        )
        file_handler.setLevel(logging.INFO)

        # Error file handler
        error_handler = RotatingFileHandler(
            os.path.join(log_dir, 'error.log'),
            maxBytes=5*1024*1024,  # 5MB
            backupCount=5
        )
        error_handler.setLevel(logging.ERROR)

        # Create formatters and add it to handlers
        log_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(log_format)
        error_handler.setFormatter(log_format)

        # Add handlers to the logger
        logger.addHandler(file_handler)
        logger.addHandler(error_handler)

    except (OSError, IOError) as e:
        # If we can't create log files, set up console logging instead
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        logger.warning(f"Could not set up file logging: {str(e)}")

    return logger 