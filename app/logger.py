import logging
import sys


def setup_logger(name, log_level=logging.INFO, log_file=None):
    """
    Set up and configure a logger.

    Args:
        name (str): The name of the logger.
        log_level (int): The logging level (e.g., logging.INFO, logging.DEBUG).
        log_file (str, optional): The file to which logs will be written. If None, logs are printed to console.

    Returns:
        logging.Logger: A configured logger instance.
    """
    # Create a logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # Create a formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Create a handler for console output
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    # Add the console handler to the logger
    logger.addHandler(console_handler)

    # If a log file is specified, add a file handler
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


logger = setup_logger("my_logger", log_level=logging.DEBUG, log_file="app.log")
