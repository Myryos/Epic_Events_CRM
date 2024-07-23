from functools import wraps
import typer
import sentry_sdk
from config import logger
from controllers.employee_controller import EmployeeController
from models.employee import Employee


def with_authenticated_employee(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        employee = EmployeeController.check_token()
        if employee:
            return func(employee, *args, **kwargs)
        else:
            raise PermissionError("User is not connected")

    return decorator


def require_manager(func):
    @wraps(func)
    def decorator(employee, *args, **kwargs):
        if employee.role == Employee.MANAGER:
            return func(employee, *args, **kwargs)
        else:
            raise PermissionError(
                "User is not authorized. Only managers can perform this action."
            )

    return decorator


def log_exceptions(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"An error has occurred: {e}", exc_info=True)
            raise

    return decorator
