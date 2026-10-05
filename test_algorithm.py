from main import Employee
from algorithm import merge_sort_employees


def test_merge_sort_employees():

    employees = [
        Employee("E001", "Vaishnavi", "v@gmail.com", "AI&DS", 65000),
        Employee("E002", "Ravi", "r@gmail.com", "IT", 40000),
        Employee("E003", "Anjali", "a@gmail.com", "HR", 80000),
    ]

    sorted_employees = merge_sort_employees(employees)

    assert sorted_employees[0].salary == 40000
    assert sorted_employees[1].salary == 65000
    assert sorted_employees[2].salary == 80000