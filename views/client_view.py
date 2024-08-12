import inquirer
import re


class ClientView:

    @classmethod
    def new_client_view(cls):
        new_client_question = [
            inquirer.Text(name="full_name", message="What is the name of the client ?"),
            inquirer.Text(
                name="email",
                message="What is the email of your client ?",
                validate=lambda _, e: cls.validate_email(e),
            ),
            inquirer.Text(
                name="phone",
                message="What is the phone number of your client ?",
                validate=lambda _, pn: cls.validate_phonenumber(pn),
            ),
            inquirer.Text(
                name="enterprise",
                message="What is name of the enterprise of your client ?",
            ),
        ]

        new_client_answer = inquirer.prompt(new_client_question)

        return new_client_answer

    @classmethod
    def choose_a_client_modify(cls, clients):
        client_to_modify = [
            inquirer.List(
                name="client",
                message="Which client do you want to modify ?",
                choices=clients,
            )
        ]

        answer = inquirer.prompt(client_to_modify)

        return answer["client"]

    @classmethod
    def choose_client_delete(cls, clients):
        client_to_delete = [
            inquirer.List(
                name="client",
                message="Which client do you want to delete ?",
                choices=clients,
            )
        ]

        answer = inquirer.prompt(client_to_delete)

        return answer["client"]

    @classmethod
    def choose_client(cls, clients):
        client_to_show = [
            inquirer.List(
                name="client",
                message="Which client do you want to display ?",
                choices=clients,
            )
        ]

        answer = inquirer.prompt(client_to_show)

        return answer["client"]

    @classmethod
    def client_field_to_modify(cls):
        client_field = [
            inquirer.List(
                name="client_field",
                message="Which client field do you want to modify ?",
                choices=[
                    "Full Name",
                    "Email",
                    "Phone",
                    "Contact",
                    "Enterprise",
                    "None",
                ],
            )
        ]

        answer = inquirer.prompt(client_field)

        return answer["client_field"]

    @classmethod
    def ask_new_full_name(cls):
        new_name_question = [
            inquirer.Text(name="new_fullname", message="What is the new name ?")
        ]

        new_name_answer = inquirer.prompt(new_name_question)

        return new_name_answer["new_fullname"]

    @classmethod
    def ask_new_email(cls):
        new_email_question = [
            inquirer.Text(
                name="email",
                message="What is your email ?",
                validate=lambda _, e: cls.validate_email(e),
            )
        ]
        new_email_answer = inquirer.prompt(new_email_question)
        return new_email_answer["email"]

    @classmethod
    def ask_new_phonenumber(cls):
        new_phonenumber_question = [
            inquirer.Text(
                name="phone",
                message="What is the new phone number ?",
                validate=lambda _, pn: cls.validate_phonenumber(pn),
            )
        ]
        new_phonenumber_answer = inquirer.prompt(new_phonenumber_question)

        return new_phonenumber_answer["phone"]

    @classmethod
    def ask_new_contact(cls, contacts):
        new_contact_question = [
            inquirer.List(
                name="contact", message="Who is the new contact ?", choices=contacts
            )
        ]

        new_contact_answer = inquirer.prompt(new_contact_question)

        return new_contact_answer["contact"]

    @classmethod
    def ask_new_enterprise(cls):
        new_enterprise_question = [
            inquirer.Text(
                name="enterprise",
                message="What is the new name for the enterprise field ?",
            )
        ]

        new_enterprise_answer = inquirer.prompt(new_enterprise_question)

        return new_enterprise_answer["enterprise"]

    @classmethod
    def display_clients(cls, clients):
        for client in clients:
            print(f"Full Name: {client}")

    @classmethod
    def display_client(cls, client):
        print(
            f"Full Name: {client.full_name}, Email: {client.email},"
            f"Creation Time: {client.creation_time}, Update Time: {client.update_time}"
        )

    @classmethod
    def display_message(cls, message):
        print(f"\n{message}\n")

    @staticmethod
    def validate_email(email: str):
        return re.fullmatch(
            r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+", email
        )

    @staticmethod
    def validate_phonenumber(phonenumber: str):
        return re.fullmatch(
            r"^(?:(?:\+|00)33[\s.-]{0,3}(?:\(0\)[\s.-]{0,3})?|0)[1-9](?:(?:[\s.-]?\d{2}){4}|\d{2}(?:[\s.-]?\d{3}){2})$",
            phonenumber,
        )
