import inquirer
import re


class ContractView:

    @classmethod
    def new_contract_view(cls, clients):
        new_contract_question = [
            inquirer.List(
                name="client_id", message="Select a client:", choices=clients
            ),
            inquirer.Text(name="total_amount", message="Total amount:"),
            inquirer.Text(name="remaining_amount", message="Remaining amount:"),
            inquirer.List(
                name="status",
                message="Contract status:",
                choices=["Pending", "Signed", "Cancelled"],
            ),
        ]

        new_contract_answer = inquirer.prompt(new_contract_question)
        new_contract_answer["total_amount"] = float(new_contract_answer["total_amount"])
        new_contract_answer["remaining_amount"] = float(
            new_contract_answer["remaining_amount"]
        )

        return new_contract_answer

    @classmethod
    def choose_contract_modify(cls, contracts):
        contract_choices = [(contract.id, str(contract)) for contract in contracts]
        contract_to_modify = [
            inquirer.List(
                name="contract",
                message="Which contract do you want to modify?",
                choices=contract_choices,
            )
        ]

        answer = inquirer.prompt(contract_to_modify)
        return answer["contract"]

    @classmethod
    def choose_contract_delete(cls, contracts):
        contract_choices = [(contract.id, str(contract)) for contract in contracts]
        contract_to_delete = [
            inquirer.List(
                name="contract",
                message="Which contract do you want to delete?",
                choices=contract_choices,
            )
        ]

        answer = inquirer.prompt(contract_to_delete)
        return answer["contract"]

    @classmethod
    def choose_contract(cls, contracts):
        contract_choices = [(contract.id, str(contract)) for contract in contracts]
        contract_to_show = [
            inquirer.List(
                name="contract",
                message="Which contract do you want to display?",
                choices=contract_choices,
            )
        ]

        answer = inquirer.prompt(contract_to_show)
        return answer["contract"]

    @classmethod
    def contract_field_to_modify(cls):
        contract_field = [
            inquirer.List(
                name="contract_field",
                message="Which contract field do you want to modify?",
                choices=[
                    "Total Amount",
                    "Remaining Amount",
                    "Status",
                    "Sales Person",
                    "None",
                ],
            )
        ]

        answer = inquirer.prompt(contract_field)
        return answer["contract_field"]

    @classmethod
    def ask_new_total_amount(cls):
        new_amount_question = [
            inquirer.Text(name="total_amount", message="What is the new total amount?")
        ]

        new_amount_answer = inquirer.prompt(new_amount_question)
        return float(new_amount_answer["total_amount"])

    @classmethod
    def ask_new_remaining_amount(cls):
        new_amount_question = [
            inquirer.Text(
                name="remaining_amount", message="What is the new remaining amount?"
            )
        ]

        new_amount_answer = inquirer.prompt(new_amount_question)
        return float(new_amount_answer["remaining_amount"])

    @classmethod
    def ask_new_status(cls):
        new_status_question = [
            inquirer.List(
                name="status",
                message="What is the new status?",
                choices=["Pending", "Signed", "Cancelled"],
            )
        ]

        new_status_answer = inquirer.prompt(new_status_question)
        return new_status_answer["status"]

    @classmethod
    def ask_new_sales_person(cls, employees):
        employee_choices = [(employee.id, employee.full_name) for employee in employees]
        new_sales_person_question = [
            inquirer.List(
                name="sales_person",
                message="Who is the new sales person?",
                choices=employee_choices,
            )
        ]

        new_sales_person_answer = inquirer.prompt(new_sales_person_question)
        return new_sales_person_answer["sales_person"]

    @classmethod
    def display_all_contracts(cls, contracts):
        for contract in contracts:
            print(
                f"Client: {contract.client.full_name}, Total Amount: {contract.total_amount}, Remaining Amount: {contract.remaining_amount}, Date: {contract.date}, Status: {contract.status}"
            )

    @classmethod
    def display_one_contract(cls, contract):
        print(
            f"Client: {contract.client.full_name}, Total Amount: {contract.total_amount}, Remaining Amount: {contract.remaining_amount}, Date: {contract.date}, Status: {contract.status}"
        )

    @classmethod
    def contract_creation_success(cls):
        print("Contract successfully created.")

    @classmethod
    def contract_modification_success(cls):
        print("Contract successfully modified.")

    @classmethod
    def contract_deletion_success(cls):
        print("Contract successfully deleted.")
