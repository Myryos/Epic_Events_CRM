import pytest
from peewee import SqliteDatabase, DoesNotExist
from models.event import Event
from models.contract import Contract
from models.employee import Employee
from models.client import Client
from controllers.event_controller import EventController
from views.event_view import EventView
from datetime import datetime

test_db = SqliteDatabase(":memory:")


@pytest.fixture
def employee_fixture():
    with test_db.bind_ctx([Employee, Client, Contract]):
        test_db.create_tables([Employee, Client, Contract, Event])
        employee = Employee(
            full_name="Jane Doe", email="jane.doe@example.com", role=Employee.SUPPORT
        )
        employee.set_password("Password234")
        employee.save()
        yield employee
        test_db.drop_tables([Employee, Client, Contract, Event])


@pytest.fixture
def contract_fixture(client_fixture, employee_fixture):
    contract = Contract(
        client=client_fixture,
        sales_person=employee_fixture,
        total_amount=10000.0,
        remaining_amount=5000.0,
        date=datetime.now(),
        status=Contract.SIGNED,
    )
    contract.save()
    yield contract


@pytest.fixture
def event_fixture(contract_fixture, employee_fixture):
    event = Event(
        full_name="Annual Meeting",
        contract=contract_fixture,
        support=employee_fixture,
        date_start=datetime(2023, 12, 25),
        date_end=datetime(2023, 12, 26),
        location="Conference Hall A",
        attendees=100,
        notes="All executives will attend.",
    )
    event.save()
    yield event


@pytest.fixture
def client_fixture(employee_fixture):
    with test_db.bind_ctx([Client]):
        client = Client(
            full_name="Test Corp",
            email="testcorp@example.com",
            phone="+33123456789",
            enterprise="Test Corp Ltd.",
            creation_time=datetime.now(),
            update_time=datetime.now(),
            contact=employee_fixture,
        )
        client.save()
        yield client


def test_create_event(mocker, employee_fixture, contract_fixture):
    # Mocking the EventView to return predefined data
    mocker.patch(
        "views.event_view.EventView.new_event_view",
        return_value={
            "full_name": "Annual Meeting",
            "contract_id": contract_fixture,
            "date_start": datetime(2023, 12, 25).date(),
            "date_end": datetime(2023, 12, 26).date(),
            "location": "Conference Hall A",
            "attendees": 100,
            "notes": "All executives will attend.",
        },
    )

    EventController.new_event(employee=employee_fixture)

    new_event = Event.get(Event.full_name == "Annual Meeting")

    assert new_event is not None
    assert new_event.contract == contract_fixture
    assert new_event.location == "Conference Hall A"
    assert new_event.attendees == 100


def test_modify_event(mocker, event_fixture, employee_fixture):
    # Mock the EventView to simulate modifying the location of the event
    mocker.patch(
        "views.event_view.EventView.choose_event_modify", return_value=event_fixture
    )
    mocker.patch(
        "views.event_view.EventView.event_field_to_modify", return_value="Location"
    )
    mocker.patch(
        "views.event_view.EventView.ask_new_location",
        return_value="New Conference Hall B",
    )

    EventController.modify_event(employee=employee_fixture)

    modified_event = Event.get_by_id(event_fixture.id)
    assert modified_event.location == "New Conference Hall B"


def test_delete_event(mocker, event_fixture, employee_fixture):
    # Mock the EventView to simulate choosing the event to delete
    mocker.patch(
        "views.event_view.EventView.choose_event_delete", return_value=event_fixture
    )

    EventController.delete_event(employee=employee_fixture)

    with pytest.raises(DoesNotExist):
        Event.get_by_id(event_fixture.id)
