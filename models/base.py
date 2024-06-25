from peewee import Model, SqliteDatabase
from config import Config

db = SqliteDatabase(Config.DATABASE["name"])


class BaseModel(Model):
    class Meta:
        database = db
