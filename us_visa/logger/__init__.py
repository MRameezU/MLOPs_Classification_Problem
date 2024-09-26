"""
Follow from:
*_  https://docs.python.org/3/library/logging.html
*_  https://docs.python.org/3/howto/logging.html
"""

# Importing the logging module to enable logging functionality in the script
import logging

# Importing the os module, which provides a way to interact with the operating system, such as file handling
import os

# Importing from_root, a utility to help determine the root directory of the project (from_root must be installed and available)
from from_root import from_root

# Importing datetime to work with date and time functions
from datetime import datetime

# Creating a log file name with the current date and time to ensure it is unique
# Example format: "09_27_2024_14_35_12.log"
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# Defining the directory name where log files will be stored
log_dir = 'logs'

# Creating the full path to the log file by joining the project's root directory, the logs directory, and the log file name
logs_path = os.path.join(from_root(), log_dir, LOG_FILE)

# Creating the 'logs' directory if it doesn't already exist; 'exist_ok=True' means no error if the directory is already there
os.makedirs(name=log_dir, exist_ok=True)

# Setting up basic configuration for logging:
# - filename: Specifies the file to write log messages to
# - format: Defines how log messages will be formatted, showing the time, logger name, level, and the actual message
# - level: Sets the minimum level of messages to log; DEBUG means log everything (DEBUG, INFO, WARNING, ERROR, CRITICAL)
logging.basicConfig(
    filename=logs_path,
            # %(asctime)s: Shows the time when the log entry was created.
            # %(name)s: Shows the name of the logger.
            # %(levelname)s: Displays the level of the log (e.g., DEBUG, INFO, WARNING, ERROR, CRITICAL).
            # %(message)s: Shows the actual log message.
    format="[%(asctime)s] %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,
)
