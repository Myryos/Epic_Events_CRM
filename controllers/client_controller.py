from models.client import Client
from controllers.employee_controller import EmployeeController
from views.client_view import ClientView

import datetime


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
    def modify_client(cls):
        clients = list(Client.select())

        client = ClientView.choose_a_client_modify(clients=clients)

        client_field = ClientView.client_field_to_modify()

        if client_field == "Full Name":
            new_name = ClientView.ask_new_full_name()
            client.full_name = new_name
        elif client_field == "Email":
            new_mail = ClientView.ask_new_email()
            client.email = new_mail
        elif client_field == "Phone":
            new_phonenumber = ClientView.ask_new_phonenumber()
            client.phone = new_phonenumber
        elif client_field == "Contact":
            contacts = EmployeeController.get_all_employee()
            new_contact = ClientView.ask_new_contact(contacts=contacts)
            client.contact = new_contact.id
        elif client_field == "Enterprise":
            new_enterprise = ClientView.ask_new_enterprise()
            client.enterprise = new_enterprise
        elif client_field == "None":
            return None

        client.save()

        # Ajouter un message de fin dans la view

    @classmethod
    def delete_client(cls):
        clients = list(Client.select())
        client = ClientView.choose_client_delete(clients=clients)

        Client.delete_by_id(client.id)
        # Ajouter un message de fin dans la view

    @classmethod
    def show_all_clients(cls):
        clients = list(Client.select())
        ClientView.display_all_client(clients=clients)

    @classmethod
    def show_one_client(cls):
        clients = list(Client.select())
        client = ClientView.choose_client(clients=clients)

        ClientView.display_one_client(client=client)
