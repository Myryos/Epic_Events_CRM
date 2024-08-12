# tests/test_employee_controller.py

import pytest
from models.employee import Employee
from peewee import DoesNotExist
from controllers.employee_controller import EmployeeController


def test_create_employee(db, mocker, logged_in_employee):
    # Mock la vue pour retourner des valeurs prédéfinies
    mocker.patch(
        "views.employee_view.EmployeeView.ask_employee_details",
        return_value={
            "full_name": "Jane Doe",
            "email": "jane.doe@example.com",
            "employee_role": "Manager",
            "confirm_password": "securePassword1",
        },
    )

    # Mock `_get_role_id` pour s'assurer qu'il retourne le bon ID de rôle
    mocker.patch(
        "controllers.employee_controller.EmployeeController._get_role_id",
        return_value=Employee.MANAGER,
    )

    EmployeeController.create_employee()

    # Vérifie que l'employé a été créé
    employee = Employee.get(Employee.email == "jane.doe@example.com")
    assert employee.full_name == "Jane Doe"
    assert employee.role == Employee.MANAGER
    assert employee.check_password("securePassword1")


def test_login_employee_success(db, mocker, logged_in_employee):
    # Mock la vue pour retourner les identifiants de connexion
    mocker.patch(
        "views.employee_view.EmployeeView.ask_employee_credentials",
        return_value={"email": logged_in_employee.email, "password": "password123"},
    )

    # Teste la connexion réussie
    token = EmployeeController.login_employee()
    assert token is not None


def test_login_employee_failure(db, mocker):
    # Mock la vue pour retourner de mauvais identifiants
    mocker.patch(
        "views.employee_view.EmployeeView.ask_employee_credentials",
        return_value={"email": "wrong.email@example.com", "password": "wrongPassword"},
    )

    # Mock l'exception lors de la recherche de l'employé
    mocker.patch("models.employee.Employee.get", side_effect=DoesNotExist)

    # Teste la connexion échouée
    token = EmployeeController.login_employee()
    assert token is None


def test_modify_employee(db, mocker, logged_in_employee):
    # Mock pour choisir un employé et la modification du champ
    mocker.patch(
        "views.employee_view.EmployeeView.choose_employee",
        return_value=logged_in_employee,
    )
    mocker.patch(
        "views.employee_view.EmployeeView.ask_employeefield_modfied",
        return_value="Full Name",
    )
    mocker.patch(
        "views.employee_view.EmployeeView.ask_new_full_name", return_value="John Smith"
    )

    EmployeeController.modify_employee()

    # Vérifie que l'employé a été modifié
    employee = Employee.get(Employee.id == logged_in_employee.id)
    assert employee.full_name == "John Smith"


def test_delete_employee(db, mocker, logged_in_employee):
    # Mock pour choisir l'employé à supprimer
    mocker.patch(
        "views.employee_view.EmployeeView.choose_employee",
        return_value=logged_in_employee,
    )

    EmployeeController.delete_employee()

    # Vérifie que l'employé a été supprimé
    with pytest.raises(DoesNotExist):
        Employee.get(Employee.id == logged_in_employee.id)
