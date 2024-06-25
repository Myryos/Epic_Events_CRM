from .base import db

from .client import Client
from .contract import Contract
from .employee import Employee
from .event import Event


def create_table():
    with db:
        db.create_tables([Client, Contract, Employee, Event])
