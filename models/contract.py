from peewee import IntegerField, FloatField, TimestampField, ForeignKeyField
from .base import BaseModel
from .client import Client
from .employee import Employee


class Contract(BaseModel):
    id = IntegerField(primary_key=True)
    client = ForeignKeyField(Client, backref="contracts", on_delete="CASCADE")
    sales_person = ForeignKeyField(Employee, backref="contracts")
    total_amount = FloatField()
    remaining_amout = FloatField()
    date = TimestampField()
    status = IntegerField()

    class Meta:
        table_name = "contract"
