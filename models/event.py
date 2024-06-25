from peewee import ForeignKeyField, IntegerField, CharField, DateField, TextField
from .base import BaseModel
from .client import Client
from .employee import Employee
from .contract import Contract


class Event(BaseModel):
    id = IntegerField(primary_key=True)
    full_name = CharField(max_length=64)
    contract = ForeignKeyField(Contract, backref="contract")
    client = ForeignKeyField(Client, backref="client")
    support = ForeignKeyField(Employee, backref="employee")
    date_start = DateField()
    date_end = DateField
    location = CharField(max_length=128)
    attendees = IntegerField
    notes = TextField()
