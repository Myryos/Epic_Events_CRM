from peewee import IntegerField, FloatField, TimestampField, ForeignKeyField
from .base import BaseModel
from .client import Client
from .employee import Employee

from datetime import datetime


class Contract(BaseModel):
    PENDING = 1
    SIGNED = 2
    CANCELLED = 3

    STATUS_CHOICES = (
        (PENDING, "Pending"),
        (SIGNED, "Signed"),
        (CANCELLED, "Cancelled"),
    )

    id = IntegerField(primary_key=True)
    client = ForeignKeyField(Client, backref="contracts", on_delete="CASCADE")
    sales_person = ForeignKeyField(Employee, backref="contracts")
    total_amount = FloatField()
    remaining_amount = FloatField()
    date = TimestampField(default=datetime.now)
    status = IntegerField(choices=STATUS_CHOICES)

    class Meta:
        table_name = "contract"

    def __str__(self):
        return f"{self.client.full_name} - {self.date}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def is_sales_person(self, employee):
        return self.sales_person == employee
