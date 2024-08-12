import pytest
from peewee import SqliteDatabase
from models.client import Client
from models.employee import Employee
from models.contract import Contract
from models.event import Event

# Utilisation d'une base de données SQLite en mémoire pour les tests
test_db = SqliteDatabase(":memory:")


@pytest.fixture(scope="function")
def db():
    test_db.bind([Employee, Client, Contract, Event])
    test_db.connect()
    test_db.create_tables([Employee, Client, Contract, Event])
    yield test_db
    test_db.drop_tables([Employee, Client, Contract, Event])
    test_db.close()


@pytest.fixture(scope="function")
def logged_in_employee(db):
    employee = Employee(
        full_name="John Doe",
        email="john@example.com",
        role=Employee.MANAGER,
    )
    employee.set_password("password123")
    employee.save()
    token = employee.generate_jwt()
    Employee.set_token(token)

    return employee
