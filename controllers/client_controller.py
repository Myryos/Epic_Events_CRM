from models.client import Client
from models.employee import Employee
from views.client_view import ClientView

from permissions import has_permission


class ClientController:

    @classmethod
    def new_client(cls, employee):
        new_client_data = ClientView.new_client_view()

        contact = employee

        new_client = Client(
            full_name=new_client_data["full_name"],
            email=new_client_data["email"],
            phone=new_client_data["phone"],
            enterprise=new_client_data["enterprise"],
            contact=contact.id,
        )
        new_client.save()
        # Ajouter un message de fin dans la view

    @classmethod
    def _get_clients(cls):
        return list(Client.select())

    @classmethod
    def _choose_client(cls, prompt_func):
        clients = cls._get_clients()
        return prompt_func(clients=clients)

    @classmethod
    def _check_permission(cls, employee, client):
        if not has_permission(employee=employee, client=client):
            raise PermissionError("You do not have permission to perform this action.")

    @classmethod
    def _display_end_message(cls, message):
        ClientView.display_message(message)

    @classmethod
    def modify_client(cls, employee):
        client = cls._choose_client(ClientView.choose_a_client_modify)
        cls._check_permission(employee, client)

        client_field = ClientView.client_field_to_modify()

        if client_field == "Full Name":
            client.full_name = ClientView.ask_new_full_name()
        elif client_field == "Email":
            client.email = ClientView.ask_new_email()
        elif client_field == "Phone":
            client.phone = ClientView.ask_new_phonenumber()
        elif client_field == "Contact":
            contacts = list(Employee.select())
            new_contact = ClientView.ask_new_contact(contacts=contacts)
            client.contact = new_contact.id
        elif client_field == "Enterprise":
            client.enterprise = ClientView.ask_new_enterprise()
        elif client_field == "None":
            return None

        client.save()
        cls._display_end_message("Client modified successfully.")

    @classmethod
    def delete_client(cls, employee):
        client = cls._choose_client(ClientView.choose_client_delete)
        cls._check_permission(employee, client)

        Client.delete_by_id(client.id)
        cls._display_end_message("Client deleted successfully.")

    @classmethod
    def display_clients(cls):
        clients = cls._get_clients()
        ClientView.display_clients(clients=clients)

    @classmethod
    def display_client(cls):
        client = cls._choose_client(ClientView.choose_client)
        ClientView.display_client(client=client)
