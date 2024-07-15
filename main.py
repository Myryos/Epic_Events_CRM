import typer
import sentry_sdk
from models import create_table
from controllers.employee_controller import EmployeeController


app = typer.Typer()


@app.command()
def init_db():
    create_table()
    typer.echo("Tables created succesfully.")


@app.command()
def create_employee():
    if EmployeeController.check_token():
        try:
            EmployeeController.create_employee()
        except Exception as e:
            sentry_sdk.capture_exception(e)
            typer.echo(f"An error as occured : {e}")


@app.command()
def modify_employee():
    try:
        EmployeeController.modify_employee()
    except Exception as e:
        sentry_sdk.capture_exception(e)
        typer.echo(f"An error as occured : {e}")


@app.command()
def login_employee():
    try:
        EmployeeController.login_employee()
    except Exception as e:
        sentry_sdk.capture_exception(e)
        typer.echo(f"An error as occured : {e}")


@app.command()
def delete_employee():
    try:
        EmployeeController.delete_employee()
    except Exception as e:
        sentry_sdk.capture_exception(e)
        typer.echo(f"An error as occured : {e}")


@app.command()
def show_all_employee():
    try:
        EmployeeController.show_all_employee()
    except Exception as e:
        sentry_sdk.capture_exception(e)
        typer.echo(f"An error as occured : {e}")


@app.command()
def show_one_employee():
    try:
        EmployeeController.show_one_employee()
    except Exception as e:
        sentry_sdk.capture_exception(e)
        typer.echo(f"An error as occured : {e}")


@app.command()
def test_token():
    EmployeeController.test_token_controller()


if __name__ == "__main__":
    app()
