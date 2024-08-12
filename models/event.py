from peewee import ForeignKeyField, IntegerField, CharField, DateField, TextField
from .base import BaseModel
from .client import Client
from .employee import Employee
from .contract import Contract


class Event(BaseModel):
    id = IntegerField(primary_key=True)
    full_name = CharField(max_length=64)
    contract = ForeignKeyField(Contract, backref="events", on_delete='CASCADE')
    support = ForeignKeyField(Employee, backref="events", null=True)
    date_start = DateField()
    date_end = DateField()
    location = CharField(max_length=128, null=True)
    attendees = IntegerField()
    notes = TextField()

    class Meta:
        table_name = "event"

    def __str__(self):
        return self.full_name

    def is_support(self, employee):
        return self.support == employee
