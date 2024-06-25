from peewee import IntegerField, FloatField, DateField, ForeignKeyField
from .base import BaseModel
from .client import Client
from .employee import Employee


class Contract(BaseModel):
    id = IntegerField(primary_key=True)
    client = ForeignKeyField(Client, backref="client")
    sales_person = ForeignKeyField(Employee, backref="employee")
    total_amount = FloatField()
    remaining_amout = FloatField()
    date = DateField()
    status = IntegerField()

    class Meta:
        table_name = "contract"
