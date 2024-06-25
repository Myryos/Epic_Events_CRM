from peewee import CharField, IntegerField, DateField, ForeignKeyField
from .base import BaseModel
from .employee import Employee


class Client(BaseModel):
    id = IntegerField(primary_key=True)
    full_name = CharField(max_length=64)
    email = CharField(max_length=126, unique=True)
    phone = CharField(null=True, max_length=10)
    entreprise = CharField(max_length=64, unique=True)
    creation_time = DateField()
    update_time = DateField
    contact = ForeignKeyField(Employee, backref="employee")

    class Meta:
        table_name = "client"
