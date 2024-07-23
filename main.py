import typer
from models import create_table
from controllers.employee_controller import EmployeeController
from controllers.client_controller import ClientController
from decorators.decorators import (
    with_authenticated_employee,
    log_exceptions,
    require_manager,
)


app = typer.Typer()


@app.command()
@log_exceptions
def init_db():
    create_table()
    typer.echo("Tables created succesfully.")


@app.command()
@log_exceptions
@with_authenticated_employee
@require_manager
def create_employee(employee):
    EmployeeController.create_employee()


@app.command()
@log_exceptions
@with_authenticated_employee
@require_manager
def modify_employee():
    EmployeeController.modify_employee()


@app.command()
@log_exceptions
@with_authenticated_employee
@require_manager
def login_employee():
    EmployeeController.login_employee()


@app.command()
@log_exceptions
@with_authenticated_employee
@require_manager
def delete_employee():
    EmployeeController.delete_employee()


@app.command()
@log_exceptions
@with_authenticated_employee
def show_all_employee():
    EmployeeController.show_all_employee()


@app.command()
@log_exceptions
@with_authenticated_employee
def show_one_employee():
    EmployeeController.show_one_employee()


@app.command()
@log_exceptions
@with_authenticated_employee
def new_client(employee):
    ClientController.new_client()


@app.command()
@log_exceptions
@with_authenticated_employee
def modify_client():
    ClientController.modify_client()


@app.command()
@log_exceptions
@with_authenticated_employee
def delete_client():
    ClientController.delete_client()


@app.command()
@log_exceptions
@with_authenticated_employee
def display_all_clients():
    ClientController.show_all_clients()


@app.command()
@log_exceptions
@with_authenticated_employee
def display_one_client():
    ClientController.show_one_client()


if __name__ == "__main__":
    app()
