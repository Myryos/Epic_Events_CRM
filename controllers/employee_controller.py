from models.employee import Employee
from views.employee_view import EmployeeView
from datetime import datetime
import jwt


class EmployeeController:
    @classmethod
    def create_employee(cls):
        answers = EmployeeView.ask_employee_details()
        employee = Employee(
            full_name=answers["full_name"],
            email=answers["email"],
            role=answers["employee_role"],
        )
        employee.set_password(answers["confirm_password"])
        employee.save()

    @classmethod
    def login_employee(cls):
        answer = EmployeeView.ask_employee_credentials()
        employee = Employee.get(Employee.email == answer["email"])
        if employee.check_password(answer["password"]):
            token = employee.generate_jwt()
            Employee.set_token(token)
            EmployeeView.show_login_result("Login successful.")
            return token
        else:
            EmployeeView.show_login_result("Invalid credentials.")
            return None

    @classmethod
    def modify_employee(cls):
        employee_to_modify = EmployeeView.choose_employee_to_modify(
            all_employee=list(Employee.select())
        )
        employee_field = EmployeeView.ask_employeefield_modfied()

        if employee_field == "Full Name":
            new_full_name = EmployeeView.ask_new_full_name()
            employee_to_modify.full_name = new_full_name
        if employee_field == "Email":
            new_email = EmployeeView.ask_new_email()
            employee_to_modify.email = new_email
        if employee_field == "Password":
            new_password = EmployeeView.ask_new_password()
            employee_to_modify.set_password(new_password)
        if employee_field == "Role":
            new_role = EmployeeView.ask_new_role()
            employee_to_modify.role = new_role
        if employee_field == "None":
            return None
        employee_to_modify.save()

        # Ajout d'un message de fin

    @classmethod
    def delete_employee(cls):
        employee_to_delete = EmployeeView.choose_employee_to_delete(
            all_employee=Employee.get_all_employee()
        )
        Employee.delete_by_id(employee_to_delete.id)
        # Ajout d'un message de fin

    @classmethod
    def show_all_employee(cls):
        employees_to_show = Employee.get_all_employee()

        EmployeeView.show_all_employee(employees_to_show)

    @classmethod
    def show_one_employee(cls):
        employee = EmployeeView.choose_employee(
            all_employee=Employee.get_all_employee()
        )

        EmployeeView.show_one_employee(employee=employee)

    @classmethod
    def get_all_employee(cls):
        return Employee.get_all_employee()

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
            print("Invalid token.")
            return None
