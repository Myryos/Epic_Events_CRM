import os
import sentry_sdk

from dotenv import load_dotenv

load_dotenv()

sentry_sdk.init(
    dsn=os.getenv("DSN_SENTRY"),
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)


class Config:
    DATABASE = {
        "name": os.getenv("DATABASE_NAME"),
        "engine": "SqliteDatabase",
        "user": os.getenv("DATABASE_USER"),
        "password": os.getenv("DATABASE_PASSWORD"),
    }
