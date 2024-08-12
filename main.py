import typer
from models import create_table
from controllers.employee_controller import EmployeeController
from controllers.client_controller import ClientController
from controllers.contract_controller import ContractController
from controllers.event_controller import EventController
from permissions import (
    require_manager,
    require_salesman,
    require_support,
    with_authenticated_employee,
)
from log_exceptions import log_exceptions
from typing import Optional

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
def create_employee(ctx: typer.Context):
    EmployeeController.create_employee()


@app.command()
@log_exceptions
@with_authenticated_employee
@require_manager
def modify_employee(ctx: typer.Context):
    EmployeeController.modify_employee()


@app.command()
@log_exceptions
def login_employee():
    EmployeeController.login_employee()


@app.command()
@log_exceptions
@with_authenticated_employee
@require_manager
def delete_employee(ctx: typer.Context):
    EmployeeController.delete_employee()


@app.command()
@log_exceptions
@with_authenticated_employee
def display_employees(ctx: typer.Context):
    EmployeeController.display_employees()


@app.command()
@log_exceptions
@with_authenticated_employee
def display_employee(ctx: typer.Context):
    EmployeeController.display_employee()


@app.command()
@log_exceptions
@with_authenticated_employee
@require_salesman
def new_client(ctx: typer.Context):
    employee = ctx.obj["employee"]
    ClientController.new_client(employee=employee)


@app.command()
@log_exceptions
@with_authenticated_employee
@require_salesman
def modify_client(ctx: typer.Context):
    employee = ctx.obj["employee"]
    ClientController.modify_client(employee=employee)


@app.command()
@log_exceptions
@with_authenticated_employee
def delete_client(ctx: typer.Context):
    employee = ctx.obj["employee"]
    ClientController.delete_client(employee=employee)


@app.command()
@log_exceptions
@with_authenticated_employee
def display_clients(ctx: typer.Context):
    ClientController.display_clients()


@app.command()
@log_exceptions
@with_authenticated_employee
def display_client(ctx: typer.Context):
    ClientController.display_client()


@app.command()
@log_exceptions
@with_authenticated_employee
@require_salesman
def create_event(ctx: typer.Context):
    employee = ctx.obj["employee"]
    EventController.new_event(employee=employee)


@app.command()
@log_exceptions
@with_authenticated_employee
def modify_event(ctx: typer.Context):
    employee = ctx.obj["employee"]
    EventController.modify_event(employee=employee)


@app.command()
@log_exceptions
@with_authenticated_employee
@require_support
def delete_event(ctx: typer.Context):
    employee = ctx.obj["employee"]
    EventController.delete_event(employee=employee)


@app.command()
@log_exceptions
@with_authenticated_employee
def display_events(
    ctx: typer.Context, no_support: bool = False, location: Optional[str] = None
):
    employee = ctx.obj["employee"]
    EventController.display_events(
        employee=employee, no_support=no_support, location=location
    )


@app.command()
@log_exceptions
@with_authenticated_employee
def display_event(
    ctx: typer.Context, no_support: bool = False, location: Optional[str] = None
):
    employee = ctx.obj["employee"]
    EventController.display_event(
        employee=employee, no_support=no_support, location=location
    )


@app.command()
@log_exceptions
@with_authenticated_employee
@require_salesman
def create_contract(ctx: typer.Context):
    employee = ctx.obj["employee"]
    ContractController.new_contract(employee=employee)


@app.command()
@log_exceptions
@with_authenticated_employee
@require_salesman
def modify_contract(ctx: typer.Context):
    employee = ctx.obj["employee"]
    ContractController.modify_contract(employee=employee)


@app.command()
@log_exceptions
@with_authenticated_employee
@require_salesman
def delete_contract(ctx: typer.Context):
    employee = ctx.obj["employee"]
    ContractController.delete_contract(employee=employee)


@app.command()
@log_exceptions
@with_authenticated_employee
def display_contracts(
    ctx: typer.Context,
    status: Optional[int] = None,
    not_signed: Optional[bool] = None,
    not_paid: Optional[bool] = None,
):
    employee = ctx.obj["employee"]
    ContractController.display_contracts(
        employee=employee, status=status, not_signed=not_signed, not_paid=not_paid
    )


@app.command()
@log_exceptions
@with_authenticated_employee
def display_contract(
    ctx: typer.Context,
    status: Optional[int] = None,
    not_signed: Optional[bool] = None,
    not_paid: Optional[bool] = None,
):
    employee = ctx.obj["employee"]
    ContractController.display_contract(
        employee=employee, status=status, not_signed=not_signed, not_paid=not_paid
    )


if __name__ == "__main__":
    app()
