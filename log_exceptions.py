import os
from functools import wraps
from config import logger
from dotenv import load_dotenv

load_dotenv()

DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"


def log_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if DEBUG_MODE:
                logger.exception(e)
            else:
                logger.error(e)
                print("Sorry, an error as occured")

    return wrapper
