import inquirer
import re


class EmployeeView:

    @classmethod
    def ask_employee_details(cls):
        roles = ["Manager", "Salesman"]

        new_employee_questions = [
            inquirer.Text(name="full_name", message="What is your full name ?"),
            inquirer.Text(
                name="email",
                message="What is your email ?",
                validate=lambda _, e: cls.is_an_email(e),
            ),
            inquirer.Password(
                name="password",
                message="What is your password ?",
                validate=lambda _, p: cls.validate_password(p),
            ),
            inquirer.Password(
                name="confirm_password",
                message="Confirm password",
                validate=lambda answers, cp: cls.validate_confirmed_password(
                    cp, answers
                ),
            ),
            inquirer.List(
                name="employee_role",
                message="Choose th role of the employee",
                choices=roles,
            ),
        ]
        new_employee_answers = inquirer.prompt(new_employee_questions)
        return new_employee_answers

    @classmethod
    def ask_employee_credentials(cls):
        employee_cred_question = [
            inquirer.Text(name="email", message="Email ?"),
            inquirer.Password(name="password", message="Password ? "),
        ]

        employee_cred_answers = inquirer.prompt(employee_cred_question)

        return employee_cred_answers

    @classmethod
    def choose_employee_to_modify(cls, all_employee):
        employee_to_modify = [
            inquirer.List(
                "employee_to_modify",
                message="Which Employee do you want to modify ?",
                choices=all_employee,
            )
        ]

        answer = inquirer.prompt(employee_to_modify)

        return answer["employee_to_modify"]

    @classmethod
    def choose_employee_to_delete(cls, all_employee):
        employe_to_delete = [
            inquirer.List(
                name="employee_to_del",
                message="Which Employee do you want to delete ?",
                choices=all_employee,
            )
        ]

        answer = inquirer.prompt(employe_to_delete)

        return answer["employee_to_del"]

    @classmethod
    def choose_employee(cls, all_employee):
        employee_to_show = [
            inquirer.List(
                name="employee",
                message="Which Employe do you want to display ?",
                choices=all_employee,
            )
        ]

        answer = inquirer.prompt(employee_to_show)

        return answer["employee"]

    @classmethod
    def ask_employeefield_modfied(cls):
        employeefield_question = [
            inquirer.List(
                name="employee_field",
                message="Which Field do you want to modify ?",
                choices=["Full name", "Password", "Email", "Role", "None"],
            )
        ]

        employeefield_answer = inquirer.prompt(employeefield_question)

        return employeefield_answer["employee_field"]

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
                validate=lambda _, e: cls.is_an_email(e),
            )
        ]
        new_email_answer = inquirer.prompt(new_email_question)
        return new_email_answer["email"]

    @classmethod
    def ask_new_password(cls):
        new_password_question = [
            inquirer.Password(
                name="password",
                message="What is your password ?",
                validate=lambda _, p: cls.validate_password(p),
            ),
            inquirer.Password(
                name="confirm_password",
                message="Confirm password",
                validate=lambda answers, cp: cls.validate_confirmed_password(
                    cp, answers
                ),
            ),
        ]

        new_password_answer = inquirer.prompt(new_password_question)

        return new_password_answer["confirm_password"]

    @classmethod
    def ask_new_role(cls):
        roles = ["Manager", "Salesman"]

        new_role_question = [
            inquirer.List(
                name="employee_role",
                message="Choose th role of the employee",
                choices=roles,
            )
        ]

        new_role_answer = inquirer.prompt(new_role_question)

        return new_role_answer["employee_role"]

    @classmethod
    def show_login_result(cls, message):
        print(message)

    @classmethod
    def show_all_employee(cls, all_employee):
        for employee in all_employee:
            print(f"Full Name: {employee}")

    @classmethod
    def show_one_employee(cls, employee):
        print(
            f"Full Name: {employee.full_name}, Email: {employee.email}, Role: {employee.role}, "
            f"Creation Time: {employee.creation_time}, Update Time: {employee.update_time}"
        )

    @staticmethod
    def is_an_email(email: str):
        return re.fullmatch(
            r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+", email
        )

    @staticmethod
    def validate_password(password: str) -> bool:
        if len(password) < 8:
            raise inquirer.errors.ValidationError(
                message="Password must be at least 8 characters long."
            )
        if not any(char.isupper() for char in password):
            raise inquirer.errors.ValidationError(
                message="Password must contain at least one uppercase letter."
            )
        if not any(char.islower() for char in password):
            raise inquirer.errors.ValidationError(
                message="Password must contain at least one lowercase letter."
            )
        if not any(char.isdigit() for char in password):
            raise inquirer.errors.ValidationError(
                message="Password must contain at least one digit."
            )
        return True

    @staticmethod
    def validate_confirmed_password(confirmed_password: str, answers: dict) -> bool:
        password = answers.get("password")
        if confirmed_password != password:
            raise inquirer.errors.ValidationError(message="Passwords do not match.")
        return True
