from models.contract import Contract
from models.client import Client
from models.employee import Employee
from views.contract_view import ContractView
from permissions import has_permission
from typing import Optional

import datetime

class ContractController:

    @classmethod
    def _get_contracts(
        cls,
        employee: Employee,
        status: Optional[int] = None,
        not_signed: Optional[bool] = None,
        not_paid: Optional[bool] = None,
    ):
        query = Contract.select()

        if employee.role == Employee.MANAGER:
            if status is not None:
                query = query.where(Contract.status == status)
            if not_signed:
                query = query.where(Contract.status == Contract.PENDING)
            if not_paid:
                query = query.where(Contract.remaining_amount > 0)

        return list(query)

    @classmethod
    def _check_permission(cls, employee, contract):
        if (
            not has_permission(employee=employee, contract=contract)
            and employee.role != Employee.MANAGER
        ):
            raise PermissionError("You do not have permission to perform this action.")

    @classmethod
    def _display_success_message(cls, action):
        success_messages = {
            "create": ContractView.contract_creation_success,
            "modify": ContractView.contract_modification_success,
            "delete": ContractView.contract_deletion_success,
        }
        success_messages[action]()

    @classmethod
    def new_contract(cls, employee):
        clients = [(client.id, client.full_name) for client in Client.select()]
        new_contract_data = ContractView.new_contract_view(clients=clients)

        client = Client.get_by_id(new_contract_data["client_id"])
        sales_person = employee.id

        new_contract = Contract(
            client=client,
            sales_person=sales_person,
            total_amount=new_contract_data["total_amount"],
            remaining_amount=new_contract_data["remaining_amount"],
            status=new_contract_data["status"],
        )
        new_contract.save()
        cls._display_success_message("create")

    @classmethod
    def modify_contract(cls, employee):
        contracts = cls._get_contracts(employee)
        contract = ContractView.choose_contract_modify(contracts=contracts)
        cls._check_permission(employee, contract)

        contract_field = ContractView.contract_field_to_modify()

        if contract_field == "Total Amount":
            contract.total_amount = ContractView.ask_new_total_amount()
        elif contract_field == "Remaining Amount":
            contract.remaining_amount = ContractView.ask_new_remaining_amount()
        elif contract_field == "Status":
            contract.status = ContractView.ask_new_status()
        elif contract_field == "Sales Person":
            employees = list(Employee.select())
            new_sales_person = ContractView.ask_new_sales_person(employees=employees)
            contract.sales_person = new_sales_person.id
        elif contract_field == "None":
            return None

        contract.save()
        cls._display_success_message("modify")

    @classmethod
    def delete_contract(cls, employee):
        contracts = cls._get_contracts(employee)
        contract = ContractView.choose_contract_delete(contracts=contracts)
        cls._check_permission(employee, contract)

        Contract.delete_by_id(contract.id)
        cls._display_success_message("delete")

    @classmethod
    def display_contracts(
        cls,
        employee: Employee,
        status: Optional[int] = None,
        not_signed: Optional[bool] = None,
        not_paid: Optional[bool] = None,
    ):
        contracts = cls._get_contracts(employee, status, not_signed, not_paid)
        ContractView.display_contracts(contracts=contracts)

    @classmethod
    def display_contract(cls, employee: Employee):
        contracts = cls._get_contracts(employee)
        contract = ContractView.choose_contract(contracts=contracts)
        ContractView.display_contract(contract=contract)
