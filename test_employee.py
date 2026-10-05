from main import Employee, EmployeeManager, calculate_average_salary


def test_add_employee():
    manager = EmployeeManager()

    employee = Employee(
        "E001",
        "Ravi",
        "ravi@gmail.com",
        "IT",
        50000
    )

    manager.add_employee(employee)

    assert "E001" in manager.employees
    assert manager.employees["E001"].name == "Ravi"


def test_search_employee():
    manager = EmployeeManager()

    employee = Employee(
        "E001",
        "Ravi",
        "ravi@gmail.com",
        "IT",
        50000
    )

    manager.add_employee(employee)

    assert manager.employees.get("E001") == employee


def test_update_employee():
    manager = EmployeeManager()

    employee = Employee(
        "E001",
        "Ravi",
        "ravi@gmail.com",
        "IT",
        50000
    )

    manager.add_employee(employee)

    manager.update_employee(
        "E001",
        "Ravi Kumar",
        "ravikumar@gmail.com",
        "HR",
        60000
    )

    assert manager.employees["E001"].name == "Ravi Kumar"
    assert manager.employees["E001"].department == "HR"
    assert manager.employees["E001"].salary == 60000


def test_delete_employee():
    manager = EmployeeManager()

    employee = Employee(
        "E001",
        "Ravi",
        "ravi@gmail.com",
        "IT",
        50000
    )

    manager.add_employee(employee)

    manager.delete_employee("E001")

    assert "E001" not in manager.employees


def test_average_salary():
    manager = EmployeeManager()

    manager.add_employee(
        Employee(
            "E001",
            "Ravi",
            "ravi@gmail.com",
            "IT",
            50000
        )
    )

    manager.add_employee(
        Employee(
            "E002",
            "Vaishu",
            "vaishu@gmail.com",
            "HR",
            70000
        )
    )

    average = calculate_average_salary(
        manager.employees.values()
    )

    assert average == 60000