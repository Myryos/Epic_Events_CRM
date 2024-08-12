import inquirer

import datetime


class EventView:

    @classmethod
    def new_event_view(cls, contracts):
        new_event_question = [
            inquirer.Text(name="full_name", message="Event name:"),
            inquirer.List(
                name="contract_id", message="Select a contract:", choices=contracts
            ),
            inquirer.Text(name="date_start", message="Start date (YYYY-MM-DD):"),
            inquirer.Text(name="date_end", message="End date (YYYY-MM-DD):"),
            inquirer.Text(name="location", message="Location:"),
            inquirer.Text(name="attendees", message="Number of attendees:"),
            inquirer.Text(name="notes", message="Notes:"),
        ]

        new_event_answer = inquirer.prompt(new_event_question)
        new_event_answer["date_start"] = datetime.datetime.strptime(
            new_event_answer["date_start"], "%Y-%m-%d"
        ).date()
        new_event_answer["date_end"] = datetime.datetime.strptime(
            new_event_answer["date_end"], "%Y-%m-%d"
        ).date()
        new_event_answer["attendees"] = int(new_event_answer["attendees"])

        return new_event_answer

    @classmethod
    def choose_event_modify(cls, events):
        event_choices = [(event.id, str(event)) for event in events]
        event_to_modify = [
            inquirer.List(
                name="event",
                message="Which event do you want to modify?",
                choices=event_choices,
            )
        ]

        answer = inquirer.prompt(event_to_modify)
        return answer["event"]

    @classmethod
    def choose_event_delete(cls, events):
        event_choices = [(event.id, str(event)) for event in events]
        event_to_delete = [
            inquirer.List(
                name="event",
                message="Which event do you want to delete?",
                choices=event_choices,
            )
        ]

        answer = inquirer.prompt(event_to_delete)
        return answer["event"]

    @classmethod
    def choose_event(cls, events):
        event_choices = [(event.id, str(event)) for event in events]
        event_to_show = [
            inquirer.List(
                name="event",
                message="Which event do you want to display?",
                choices=event_choices,
            )
        ]

        answer = inquirer.prompt(event_to_show)
        return answer["event"]

    @classmethod
    def event_field_to_modify(cls):
        event_field = [
            inquirer.List(
                name="event_field",
                message="Which event field do you want to modify?",
                choices=[
                    "Full Name",
                    "Date Start",
                    "Date End",
                    "Location",
                    "Attendees",
                    "Notes",
                    "Support",
                    "None",
                ],
            )
        ]

        answer = inquirer.prompt(event_field)
        return answer["event_field"]

    @classmethod
    def ask_new_full_name(cls):
        new_name_question = [
            inquirer.Text(name="full_name", message="What is the new name?")
        ]

        new_name_answer = inquirer.prompt(new_name_question)
        return new_name_answer["full_name"]

    @classmethod
    def ask_new_date_start(cls):
        new_date_question = [
            inquirer.Text(
                name="date_start", message="What is the new start date (YYYY-MM-DD)?"
            )
        ]

        new_date_answer = inquirer.prompt(new_date_question)
        return datetime.datetime.strptime(
            new_date_answer["date_start"], "%Y-%m-%d"
        ).date()

    @classmethod
    def ask_new_date_end(cls):
        new_date_question = [
            inquirer.Text(
                name="date_end", message="What is the new end date (YYYY-MM-DD)?"
            )
        ]

        new_date_answer = inquirer.prompt(new_date_question)
        return datetime.datetime.strptime(
            new_date_answer["date_end"], "%Y-%m-%d"
        ).date()

    @classmethod
    def ask_new_location(cls):
        new_location_question = [
            inquirer.Text(name="location", message="What is the new location?")
        ]

        new_location_answer = inquirer.prompt(new_location_question)
        return new_location_answer["location"]

    @classmethod
    def ask_new_attendees(cls):
        new_attendees_question = [
            inquirer.Text(
                name="attendees", message="What is the new number of attendees?"
            )
        ]

        new_attendees_answer = inquirer.prompt(new_attendees_question)
        return int(new_attendees_answer["attendees"])

    @classmethod
    def ask_new_notes(cls):
        new_notes_question = [
            inquirer.Text(name="notes", message="What are the new notes?")
        ]

        new_notes_answer = inquirer.prompt(new_notes_question)
        return new_notes_answer["notes"]

    @classmethod
    def ask_new_support(cls, employees):
        employee_choices = [(employee.id, employee.full_name) for employee in employees]
        new_support_question = [
            inquirer.List(
                name="support",
                message="Who is the new support?",
                choices=employee_choices,
            )
        ]

        new_support_answer = inquirer.prompt(new_support_question)
        return new_support_answer["support"]

    @classmethod
    def display_events(cls, events):
        for event in events:
            print(
                f"Event: {event.full_name}, Start: {event.date_start}, End: {event.date_end}, Location: {event.location}, Attendees: {event.attendees}"
            )

    @classmethod
    def display_event(cls, event):
        print(
            f"Event: {event.full_name}, Start: {event.date_start}, End: {event.date_end}, Location: {event.location}, Attendees: {event.attendees}, Notes: {event.notes}"
        )

    @classmethod
    def event_creation_success(cls):
        print("Event successfully created.")

    @classmethod
    def event_modification_success(cls):
        print("Event successfully modified.")

    @classmethod
    def event_deletion_success(cls):
        print("Event successfully deleted.")
