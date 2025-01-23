# Epic Events CRM

## 1. Why
After organizing hundreds of events, our team realized the need for an efficient Customer Relationship Management (CRM) system. Our current tools are inadequate, leading to challenges in managing client information and event data.

To improve our operations and rebuild client trust, we are developing a secure internal CRM system. This new system will help us securely store and manage client information, contracts, and events, ensuring that our processes are both efficient and reliable. By adopting this proactive approach, we aim to demonstrate our commitment to excellence and enhance our service quality.
## 2. Getting Started

This project utilizes the following technologies:

- Python 3.10
- Peewee
- Typer
- Sentry SDK
- Inquirer
- InquirerPy
- Bcrypt
- Cryptography
- Python-dotenv
- PyJWT

## 3. Installation

1. **Clone the repository** and navigate into the project directory.

    ``` git clone https://github.com/Myryos/Epic_Events_CRM.git```
    and
    ``` cd Epic_Events_CRM ```

2. **Set up a virtual environment**:
    ```poetry env use python3.10```

3. **Activate the virtual environment**:
   
   Poetry automatically handles the activation of the virtual environment when running poetry commands, so this step is implicitly covered.

4. **Install required packages**

    ```poetry install```
    
5. **Set the database.**
    use the command bellow for setup the database : 

    ```poetry run python main.py init-db```
   
6. **How to use the application**

   ***Employee Management***

    login_employee: Log in as an employee.

    ```
    poetry run python main.py login-employee
    ```

    create_employee: Create a new employee (requires manager privileges).

    ```
    poetry run python main.py create-employee
    ```

    modify_employee: Modify an existing employee (requires manager privileges).

    ```
    poetry run python main.py modify-employee
    ```

    delete_employee: Delete an employee (requires manager privileges).

    ```
    poetry run python main.py delete-employee
    ```

    display_employees: Display all employees.

    ```
    poetry run python main.py display-employees 
    ```

    display_employee: Display a specific employee.

    ```
    poetry run python main.py display-employee
    ```

    ***Client Management***

    new_client: Add a new client.

    ```
    poetry run python main.py new-client
    ```

    modify_client: Modify an existing client.

    ```
    poetry run python main.py modify-client
    ```

    delete_client: Delete a client.

    ```
    poetry run python main.py delete-client
    ```

    display_clients: Display all clients.

    ```
    poetry run python main.py display-clients
    ```

    display_client: Display a specific client.

    ```
    poetry run python main.py display-client
    ```

    ***Event Management***

    create_event: Create a new event (requires manager privileges).

    ```
    poetry run python main.py create-event
    ```

    modify_event: Modify an existing event (requires manager privileges).

    ```
    poetry run python main.py modify-event
    ```

    delete_event: Delete an event (requires manager privileges).

    ```
    poetry run python main.py delete-event
    ```

    display_events: Display all events.

    ```
    poetry run python main.py display-events [OPTIONS]
    ```
    Options : 
    - employee: Filter events by the logged-in employee.
    - no_support: Display only events without support staff.
    - location: Filter events by location.

    display_event: Display a specific event.

    ```
    poetry run python main.py display-event [OPTIONS]
    ```
    Options : 
    - employee: Filter events by the logged-in employee.
    - no_support: Display only events without support staff.
    - location: Filter events by location.

    ***Contract Management***

    create_contract: Create a new contract.

    ```
    poetry run python main.py create-contract
    ```

    modify_contract: Modify an existing contract (requires manager privileges).

    ```
    poetry run python main.py modify-contract
    ```

    delete_contract: Delete a contract (requires manager privileges).

    ```
    poetry run python main.py delete-contract
    ```

    display_contracts: Display all contracts.

    ```
    poetry run python main.py display-contracts [OPTIONS]
    ```
    Options:

    - employee: Filter contracts by the logged-in employee.
    - status: Filter contracts by their status.
    - not_signed: Display only unsigned contracts.
    - not_paid: Display only unpaid contracts

    display_contract: Display a specific contract.

    ```
    poetry run python main.py display-contract [OPTIONS]
    ```
    Options:

    - employee: Filter contracts by the logged-in employee.
    - status: Filter contracts by their status.
    - not_signed: Display only unsigned contracts.
    - not_paid: Display only unpaid contracts


7. **.ENV**
   An .env file is required for environment-specific configurations such as database settings. This file can be provided by the creator via email.
