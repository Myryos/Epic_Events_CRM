from models.event import Event
from models.contract import Contract
from models.employee import Employee
from views.event_view import EventView
from permissions import has_permission
from typing import Optional


class EventController:

    @staticmethod
    def _get_filtered_events(
        employee, no_support: bool = False, location: Optional[str] = None
    ):
        query = Event.select()
        if employee.role == Employee.MANAGER:
            if no_support:
                query = query.where(Event.support.is_null(True))
            if location:
                query = query.where(Event.location == location)
        return list(query)

    @staticmethod
    def _check_event_permission(employee, event):
        if not (
            has_permission(employee=employee, event=event)
            or employee.role == Employee.MANAGER
        ):
            print("You do not have permission for this event.")
            return False
        return True

    @staticmethod
    def _update_event_field(event, field):
        field_update_map = {
            "Full Name": EventView.ask_new_full_name,
            "Date Start": EventView.ask_new_date_start,
            "Date End": EventView.ask_new_date_end,
            "Location": EventView.ask_new_location,
            "Attendees": EventView.ask_new_attendees,
            "Notes": EventView.ask_new_notes,
            "Support": lambda: EventView.ask_new_support(
                employees=list(Employee.select())
            ),
        }
        if field in field_update_map:
            update_func = field_update_map[field]
            if field == "Support":
                event.support = update_func().id
            else:
                setattr(event, field.lower().replace(" ", "_"), update_func())
            event.save()
            return True
        return False

    @staticmethod
    def _display_success_message(action):
        success_messages = {
            "create": EventView.event_creation_success,
            "modify": EventView.event_modification_success,
            "delete": EventView.event_deletion_success,
        }
        success_messages.get(action, lambda: None)()

    @classmethod
    def new_event(cls, employee):
        contracts = [(contract.id, str(contract)) for contract in Contract.select()]
        new_event_data = EventView.new_event_view(contracts=contracts)

        contract = Contract.get_by_id(new_event_data["contract_id"])
        if (
            has_permission(contract=contract, employee=employee)
            and contract.status == Contract.SIGNED
        ):
            new_event = Event(
                full_name=new_event_data["full_name"],
                contract=contract,
                support=None,
                date_start=new_event_data["date_start"],
                date_end=new_event_data["date_end"],
                location=new_event_data["location"],
                attendees=new_event_data["attendees"],
                notes=new_event_data["notes"],
            )
            new_event.save()
            cls._display_success_message("create")

    @classmethod
    def modify_event(cls, employee):
        events = list(Event.select())
        event = EventView.choose_event_modify(events=events)

        if cls._check_event_permission(employee, event):
            event_field = EventView.event_field_to_modify()
            if event_field == "None":
                return None

            if cls._update_event_field(event, event_field):
                cls._display_success_message("modify")

    @classmethod
    def delete_event(cls, employee):
        events = list(Event.select())
        event = EventView.choose_event_delete(events=events)

        if has_permission(employee=employee, event=event):
            Event.delete_by_id(event.id)
            cls._display_success_message("delete")

    @classmethod
    def display_events(
        cls, employee, no_support: bool = False, location: Optional[str] = None
    ):
        events = cls._get_filtered_events(employee, no_support, location)
        EventView.display_events(events=events)

    @classmethod
    def display_event(
        cls, employee, no_support: bool = False, location: Optional[str] = None
    ):
        events = cls._get_filtered_events(employee, no_support, location)
        event = EventView.choose_event(events=events)
        EventView.display_event(event=event)
