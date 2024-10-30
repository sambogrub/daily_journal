'''Main logging configuration for the daily journal app. 
All global values can be found in config.py'''

import daily_journal.config as config

import logging
import pathlib
from logging.handlers import RotatingFileHandler

#default logger name
JOURNAL_LOGGER_NAME = 'journal'

def configure_logger(
        name = JOURNAL_LOGGER_NAME,
        log_file = config.LOGGING_FILE_NAME,
        level = config.LOGGING_LEVEL,
        size_limit = config.LOGGING_MAX_LOG_SIZE,
        backup_count = config.LOGGING_FILE_BACKUP_COUNT):
    """ Sets up the default Journal logger based on the values from config """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if not logger.hasHandlers():
        # Create folder structure for log files in case it doesn't exist yet...
        log_dir = pathlib.Path(config.LOGGING_FILE_NAME).parent
        log_dir.mkdir(parents=True, exist_ok=True)
        # Keep the logging configuration to a minimum
        handler = RotatingFileHandler(log_file, maxBytes=size_limit, backupCount=backup_count)
        handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logger.addHandler(handler)

def journal_logger():
    """
        Shortcut for retrieving default Journal logger. Logger will be
        initialized in main module.
    """
    return logging.getLogger(JOURNAL_LOGGER_NAME)