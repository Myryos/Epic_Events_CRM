import pytest
from main import init_db
from models import Employee, Client, Contract, Event


def test_init_db():
    init_db()

    assert Employee.table_exists()
    assert Client.table_exists()
    assert Contract.table_exists()
    assert Event.table_exists()
