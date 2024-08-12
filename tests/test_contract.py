import pytest
from models.contract import Contract
from models.client import Client
from models.employee import Employee
from controllers.contract_controller import ContractController
from views.contract_view import ContractView
from datetime import datetime
from peewee import SqliteDatabase

# Setting up an in-memory SQLite database for testing
test_db = SqliteDatabase(":memory:")


@pytest.fixture
def employee_fixture():
    with test_db.bind_ctx([Employee, Client, Contract]):
        test_db.create_tables([Employee, Client, Contract])
        employee = Employee(
            full_name="Jane Doe", email="jane.doe@example.com", role=Employee.SALESMAN
        )
        employee.set_password("Password234")
        employee.save()
        yield employee
        test_db.drop_tables([Employee, Client, Contract])


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


@pytest.fixture
def contract_fixture(client_fixture, employee_fixture):
    with test_db.bind_ctx([Contract]):
        contract = Contract(
            client=client_fixture,
            sales_person=employee_fixture,
            total_amount=10000.0,
            remaining_amount=5000.0,
            date=datetime.now(),
            status=Contract.PENDING,
        )
        contract.save()
        yield contract


@pytest.fixture
def contract_controller_fixture():
    return ContractController()


def test_create_contract(contract_controller_fixture, client_fixture, employee_fixture):
    # Mocking the ContractView.new_contract_view method to return predefined data
    contract_data = {
        "client_id": client_fixture,
        "total_amount": 15000.0,
        "remaining_amount": 15000.0,
        "status": Contract.PENDING,
        "sales_person": employee_fixture,
    }

    def mock_new_contract_view(clients):
        return contract_data

    ContractView.new_contract_view = mock_new_contract_view

    contract_controller_fixture.new_contract(employee=employee_fixture)

    new_contract = Contract.get(Contract.client == client_fixture)

    assert new_contract.total_amount == 15000.0
    assert new_contract.remaining_amount == 15000.0
    assert new_contract.status == Contract.PENDING


def test_modify_contract(
    contract_controller_fixture, contract_fixture, employee_fixture
):
    # Mocking the ContractView methods to return specific values
    def mock_choose_contract_modify(contracts):
        return contract_fixture

    def mock_contract_field_to_modify():
        return "Total Amount"

    def mock_ask_new_total_amount():
        return float(20000.0)

    ContractView.choose_contract_modify = mock_choose_contract_modify
    ContractView.contract_field_to_modify = mock_contract_field_to_modify
    ContractView.ask_new_total_amount = mock_ask_new_total_amount

    ContractController.modify_contract(employee=employee_fixture)

    modified_contract = Contract.get(Contract.id == contract_fixture.id)

    assert modified_contract.total_amount == float(20000.0)


def test_delete_contract(
    contract_controller_fixture, contract_fixture, employee_fixture
):
    # Mock the ContractView.choose_contract_delete method to return the contract fixture
    def mock_choose_contract_delete(contracts):
        return contract_fixture

    ContractView.choose_contract_delete = mock_choose_contract_delete

    contract_controller_fixture.delete_contract(employee=employee_fixture)

    with pytest.raises(Contract.DoesNotExist):
        Contract.get(Contract.id == contract_fixture.id)


def test_display_contracts(
    contract_controller_fixture, contract_fixture, employee_fixture
):
    # Mock the ContractView.display_contracts to check if it was called correctly
    def mock_display_contracts(contracts):
        assert len(contracts) == 1
        assert contracts[0].total_amount == 10000.0

    ContractView.display_contracts = mock_display_contracts

    contract_controller_fixture.display_contracts(employee=employee_fixture)


def test_display_contract(
    contract_controller_fixture, contract_fixture, employee_fixture
):
    # Mock the ContractView.choose_contract and display_contract methods
    def mock_choose_contract(contracts):
        return contract_fixture

    def mock_display_contract(contract):
        assert contract.total_amount == 10000.0

    ContractView.choose_contract = mock_choose_contract
    ContractView.display_contract = mock_display_contract

    contract_controller_fixture.display_contract(employee=employee_fixture)
