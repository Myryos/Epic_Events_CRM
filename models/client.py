from peewee import CharField, IntegerField, TimestampField, ForeignKeyField
from .base import BaseModel
from .employee import Employee


class Client(BaseModel):
    id = IntegerField(primary_key=True)
    full_name = CharField(max_length=64)
    email = CharField(max_length=126, unique=True)
    phone = CharField(null=True, max_length=20)
    enterprise = CharField(max_length=64)
    creation_time = TimestampField()
    update_time = TimestampField()
    contact = ForeignKeyField(Employee, backref="client")

    class Meta:
        table_name = "client"
