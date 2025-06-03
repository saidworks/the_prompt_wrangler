import logging
from pythonjsonlogger.json import JsonFormatter
import sys

# Configure the root logger
logger = logging.getLogger(__name__)  # Get a logger for the current module
logger.setLevel(logging.INFO)  # Set default log level

# Configure a stream handler to output to the console
console_handler = logging.StreamHandler(stream=sys.stdout)  # Ensures output to console
console_handler.setLevel(logging.INFO)  # Set level for console output
formatter = JsonFormatter(
    defaults={"environment": "dev", "module": __name__}  # include module name
)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


def get_logger(name, level=logging.INFO):
    """
    Returns a logger instance with specified name and level.

    Args:
        name (str): The name of the logger.  Should ideally reflect the class or module using it.
        level (int): The logging level (e.g., logging.DEBUG, logging.INFO, logging.ERROR).

    Returns:
        logging.Logger: A configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(console_handler)  # Reuse the existing console handler
    return logger


# Example usage (within a class or module):
# class MyClass:
#     _logger = get_logger("MyClass")  # Get a logger specifically for MyClass
#
#     def my_method(self):
#         self._logger.debug("Entering my_method")
#         # ... your code ...
#         self._logger.info("my_method completed successfully")
