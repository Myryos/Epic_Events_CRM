import os
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration
import logging
from dotenv import load_dotenv

load_dotenv()
sentry_logging = LoggingIntegration(
    level=logging.INFO,  # Capture info and above as breadcrumbs
    event_level=logging.ERROR,  # Send errors as events
)
sentry_sdk.init(
    dsn=os.getenv("DSN_SENTRY"),
    traces_sample_rate=0.1,
    profiles_sample_rate=0.1,
    integrations=[sentry_logging],
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

class Config:
    DATABASE = {
        "name": os.getenv("DATABASE_NAME"),
        "engine": "SqliteDatabase",
        "user": os.getenv("DATABASE_USER"),
        "password": os.getenv("DATABASE_PASSWORD"),
    }
