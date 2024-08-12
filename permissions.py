from functools import wraps
from controllers.employee_controller import EmployeeController
from models.employee import Employee
import typer
import os
from dotenv import load_dotenv
from config import logger

load_dotenv()

DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"


def with_authenticated_employee(func):
    @wraps(func)
    def wrapper(ctx: typer.Context, *args, **kwargs):
        employee = EmployeeController.check_token()
        try:
            if employee is not None:
                ctx.obj = {"employee": employee}
                return func(ctx=ctx, *args, **kwargs)
        except PermissionError as e:
            if DEBUG_MODE:
                logger.exception("An error occurred: %s", e)
            else:
                logger.error("Permission denied: %s", e)
                print(
                    "Sorry, you don't have the required permissions to perform this action."
                )

    return wrapper


def require_role(required_role):
    def decorator(func):
        @wraps(func)
        def wrapper(ctx: typer.Context, *args, **kwargs):
            employee = ctx.obj.get("employee")
            try:
                if employee and employee.role == required_role:
                    return func(ctx, *args, **kwargs)
                else:
                    raise PermissionError(
                        f"User is not authorized. Only {required_role}s can perform this action."
                    )
            except PermissionError as e:
                if DEBUG_MODE:
                    logger.exception("Permission error: %s", e)
                else:
                    logger.error(
                        "Permission denied for role '%s': %s", required_role, e
                    )
                    typer.echo(str(e))
                return None

        return wrapper

    return decorator


require_manager = require_role(Employee.MANAGER)
require_salesman = require_role(Employee.SALESMAN)
require_support = require_role(Employee.SUPPORT)


def has_permission(employee, contract=None, client=None, event=None):
    if contract and contract.is_sales_person(employee):
        return True
    elif client and client.is_contact(employee):
        return True
    elif event and event.is_support(employee):
        return True
    else:
        return False
