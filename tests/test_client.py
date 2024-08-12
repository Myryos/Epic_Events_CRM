import pytest
from models.client import Client
from models.employee import Employee
from controllers.client_controller import ClientController
from views.client_view import ClientView
from datetime import datetime
from peewee import SqliteDatabase


test_db = SqliteDatabase(":memory:")


@pytest.fixture
def employee_fixture():
    with test_db.bind_ctx([Employee, Client]):
        test_db.create_tables([Employee, Client])
        employee = Employee(
            full_name="John Client",
            email="johnclient@example.com",
            role=Employee.SALESMAN,
        )
        employee.set_password("Password123")
        employee.save()
        yield employee
        test_db.drop_tables([Employee, Client])


@pytest.fixture
def client_fixture(employee_fixture):
    with test_db.bind_ctx([Client]):
        client = Client(
            full_name="Acme Corp",
            email="acme@example.com",
            phone="+33123456789",
            enterprise="Acme",
            creation_time=datetime.now(),
            update_time=datetime.now(),
            contact=employee_fixture,
        )
        client.save()
        yield client


@pytest.fixture
def client_controller_fixture():
    return ClientController()


def test_create_client(client_controller_fixture, employee_fixture, mocker):
    # Mock la méthode new_client_view pour qu'elle retourne des données prédéfinies
    client_data = {
        "full_name": "New Client",
        "email": "newclient@example.com",
        "phone": "+33987654321",
        "enterprise": "New Enterprise",
        "contact_id": employee_fixture.id,
    }

    # Patch la méthode `new_client_view` dans `ClientView`
    mocker.patch(
        "views.client_view.ClientView.new_client_view", return_value=client_data
    )

    # Appel de la méthode pour créer un nouveau client
    ClientController.new_client(employee=employee_fixture)

    # Vérifications après la création du client
    new_client = Client.get(Client.email == "newclient@example.com")

    assert new_client.full_name == "New Client"
    assert new_client.phone == "+33987654321"
    assert new_client.enterprise == "New Enterprise"
    assert new_client.contact.id == employee_fixture.id


def test_modify_client(client_controller_fixture, client_fixture, employee_fixture):
    def mock_choose_a_client_modify(clients):
        return client_fixture

    def mock_client_field_to_modify():
        return "Full Name"

    def mock_ask_new_full_name():
        return "Modified Client"

    ClientView.choose_a_client_modify = mock_choose_a_client_modify
    ClientView.client_field_to_modify = mock_client_field_to_modify
    ClientView.ask_new_full_name = mock_ask_new_full_name

    client_controller_fixture.modify_client(employee=employee_fixture)

    modified_client = Client.get(Client.id == client_fixture.id)

    assert modified_client.full_name == "Modified Client"


def test_delete_client(client_controller_fixture, client_fixture, employee_fixture):
    def mock_choose_client_delete(clients):
        return client_fixture

    ClientView.choose_client_delete = mock_choose_client_delete

    client_controller_fixture.delete_client(employee=employee_fixture)

    with pytest.raises(Client.DoesNotExist):
        Client.get(Client.id == client_fixture.id)


def test_display_clients(client_controller_fixture, client_fixture):
    def mock_display_clients(clients):
        assert len(clients) == 1
        assert clients[0].full_name == "Acme Corp"

    ClientView.display_clients = mock_display_clients

    client_controller_fixture.display_clients()


def test_display_client(client_controller_fixture, client_fixture):
    def mock_choose_client(clients):
        return client_fixture

    def mock_display_client(client):
        assert client.full_name == "Acme Corp"

    ClientView.choose_client = mock_choose_client
    ClientView.display_client = mock_display_client

    client_controller_fixture.display_client()
