from models.contract import Contract
from models.client import Client
from controllers.employee_controller import EmployeeController
from views.contract_view import ContractView

import datetime


class ContractController:

    @classmethod
    def new_contract(cls, employee):
        clients = [(client.id, client.full_name) for client in Client.select()]
        new_contract_data = ContractView.new_contract_view(clients=clients)

        client = Client.get_by_id(new_contract_data["client_id"])
        sales_person = employee

        new_contract = Contract(
            client=client,
            sales_person=sales_person,
            total_amount=new_contract_data["total_amount"],
            remaining_amount=new_contract_data["remaining_amount"],
            status=new_contract_data["status"],
        )
        new_contract.save()
        ContractView.contract_creation_success()

    @classmethod
    def modify_contract(cls):
        contracts = list(Contract.select())
        contract = ContractView.choose_contract_modify(contracts=contracts)

        contract_field = ContractView.contract_field_to_modify()

        if contract_field == "Total Amount":
            new_amount = ContractView.ask_new_total_amount()
            contract.total_amount = new_amount
        elif contract_field == "Remaining Amount":
            new_amount = ContractView.ask_new_remaining_amount()
            contract.remaining_amount = new_amount
        elif contract_field == "Status":
            new_status = ContractView.ask_new_status()
            contract.status = new_status
        elif contract_field == "Sales Person":
            employees = EmployeeController.get_all_employee()
            new_sales_person = ContractView.ask_new_sales_person(employees=employees)
            contract.sales_person = new_sales_person.id
        elif contract_field == "None":
            return None

        contract.save()
        ContractView.contract_modification_success()

    @classmethod
    def delete_contract(cls):
        contracts = list(Contract.select())
        contract = ContractView.choose_contract_delete(contracts=contracts)

        Contract.delete_by_id(contract.id)
        ContractView.contract_deletion_success()

    @classmethod
    def show_all_contracts(cls):
        contracts = list(Contract.select())
        ContractView.display_all_contracts(contracts=contracts)

    @classmethod
    def show_one_contract(cls):
        contracts = list(Contract.select())
        contract = ContractView.choose_contract(contracts=contracts)

        ContractView.display_one_contract(contract=contract)
