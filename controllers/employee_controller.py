from models.employee import Employee
from views.employee_view import EmployeeView
from datetime import datetime
from peewee import DoesNotExist
import jwt

class EmployeeController:

    @staticmethod
    def _get_role_id(role_name_chosen):
        for role_id, role_name in Employee.ROLE_CHOICES:
            if role_name_chosen == role_name:
                return role_id
        return None

    @staticmethod
    def _get_employee_details():
        answers = EmployeeView.ask_employee_details()
        role_id = EmployeeController._get_role_id(answers["employee_role"])
        return {
            "full_name": answers["full_name"],
            "email": answers["email"],
            "role": role_id,
            "password": answers["confirm_password"],
        }

    @staticmethod
    def _choose_employee(message):
        return EmployeeView.choose_employee(
            all_employee=list(Employee.select()), message=message
        )

    @staticmethod
    def _display_success_message(action):
        success_messages = {
            "create": "Employee created successfully.",
            "modify": "Employee modified successfully.",
            "delete": "Employee deleted successfully.",
            "login": "Login successful.",
            "login_failure": "Invalid credentials.",
        }
        EmployeeView.show_login_result(success_messages.get(action, ""))

    @classmethod
    def create_employee(cls):
        details = cls._get_employee_details()
        new_employee = Employee(
            full_name=details["full_name"],
            email=details["email"],
            role=details["role"],
        )
        new_employee.set_password(details["password"])
        new_employee.save()
        cls._display_success_message("create")

    @classmethod
    def login_employee(cls):
        credentials = EmployeeView.ask_employee_credentials()
        try:
            employee = Employee.get(Employee.email == credentials["email"])
            if employee.check_password(credentials["password"]):
                return employee.generate_jwt()
        except DoesNotExist:
            return None

    @classmethod
    def modify_employee(cls):
        employee_to_modify = cls._choose_employee("Choose an employee to modify")
        employee_field = EmployeeView.ask_employeefield_modfied()

        if employee_field == "Full Name":
            employee_to_modify.full_name = EmployeeView.ask_new_full_name()
        elif employee_field == "Email":
            employee_to_modify.email = EmployeeView.ask_new_email()
        elif employee_field == "Password":
            employee_to_modify.set_password(EmployeeView.ask_new_password())
        elif employee_field == "Role":
            new_role = EmployeeView.ask_new_role()
            role_id = EmployeeController._get_role_id(new_role)
            employee_to_modify.role = role_id
        elif employee_field == "None":
            return None

        employee_to_modify.save()
        cls._display_success_message("modify")

    @classmethod
    def delete_employee(cls):
        employee_to_delete = cls._choose_employee("Choose an employee to delete")
        Employee.delete_by_id(employee_to_delete.id)
        cls._display_success_message("delete")

    @classmethod
    def display_employees(cls):
        employees_to_show = list(Employee.select())
        EmployeeView.display_employees(employees_to_show)

    @classmethod
    def display_employee(cls):
        employee = cls._choose_employee("Choose an employee to display")
        EmployeeView.display_employee(employee=employee)

    @staticmethod
    def check_token():
        token = Employee.load_token()
        employee_id = Employee.decode_jwt(token)
        if employee_id:
            try:
                employee = Employee.get(Employee.id == employee_id)
                print(f"Authenticated Employee: {employee.full_name}")
                return employee
            except Employee.DoesNotExist:
                print("Employee not found.")
                return None
        else:
            return None
