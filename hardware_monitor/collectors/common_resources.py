
import logging
from datetime import datetime

# Configure the logging system
logging.basicConfig(
    filename="/home/shamshs/Documents/work/task3_pythonModules/error_log.txt",
    level=logging.ERROR,
    format="%(asctime)s — %(levelname)s — %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def log_error(context, error):
    """Logs any error with a custom context message.
    
    Example: log_error("Monitor vendor fetch failed", e)

    Args:
        context (str): shows where the error occurred.
        error (str): exception or error message.
    """
    logging.error(f"{context}: {error}")



def convert_number(value):
    """Convert string to int if whole number,float if decimal, otherwise return original string.

    Args:
        value (float/int): number float or int to be converted if in wrong data type.

    Returns:
        value (float/int): value with fixed type float or int converted and cleaned.
    """

    if value is None:
        return None

    try:
        num = float(value)
        return int(num) if num.is_integer() else num
    except ValueError:
        return value
    
