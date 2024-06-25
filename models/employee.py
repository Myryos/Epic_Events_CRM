from peewee import IntegerField, CharField, DateField
from .base import BaseModel


class Employee(BaseModel):
    id = IntegerField(primary_key=True)
    full_name = CharField(max_length=64)
    email = CharField(max_length=128, unique=True)
    password = CharField(max_length=16)
    role = IntegerField()
    creation_time = DateField()
    update_time = DateField()

    class Meta:
        table_name = "employee"
