from peewee import IntegrityError
from .base import db

from .client import Client
from .contract import Contract
from .employee import Employee
from .event import Event


def create_table():
    with db:
        db.create_tables([Client, Contract, Employee, Event])

        if Employee.select().count() == 0:
            try:
                # Create the first employee (Manager)
                first_employee = Employee(
                    full_name="OC Exam",
                    email="exam@oc.com",
                    role=Employee.MANAGER,
                )
                first_employee.set_password("uEE0I5x1!")  # Hash and set the password
                first_employee.save()

                print(
                    f"First user created: {first_employee.full_name} ({first_employee.email})"
                )
            except IntegrityError as e:
                print(f"Error creating the first user: {e}")
        else:
            print("User(s) already exist in the database.")
