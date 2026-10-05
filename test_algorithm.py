from main import Employee

from algorithm import (
    merge_sort_employees,
    maximum_salary_with_budget,
    greedy_employee_selection,
    backtracking_team_selection,
    branch_and_bound_employee_selection,
)


# ============================================================
# TEST EMPLOYEES
# ============================================================

def create_test_employees():
    return [
        Employee(
            "E001",
            "Vaishnavi",
            "vaishnavi@gmail.com",
            "AI&DS",
            65000
        ),
        Employee(
            "E002",
            "Akki",
            "akki@gmail.com",
            "IT",
            40000
        ),
        Employee(
            "E003",
            "Shiny",
            "shiny@gmail.com",
            "HR",
            80000
        ),
        Employee(
            "E004",
            "Vamsi",
            "vamsi@gmail.com",
            "CSE",
            30000
        ),
    ]


# ============================================================
# 1. DIVIDE AND CONQUER
# MERGE SORT
# ============================================================

def test_merge_sort_employees():

    employees = create_test_employees()

    sorted_employees = merge_sort_employees(employees)

    assert sorted_employees[0].salary == 30000
    assert sorted_employees[1].salary == 40000
    assert sorted_employees[2].salary == 65000
    assert sorted_employees[3].salary == 80000


# ============================================================
# 2. DYNAMIC PROGRAMMING
# ============================================================

def test_dynamic_programming():

    employees = create_test_employees()

    selected, total = maximum_salary_with_budget(
        employees,
        100000
    )

    # Best possible combination:
    # Vaishnavi = 65000
    # Vamsi = 30000
    # Total = 95000

    assert total == 95000

    selected_ids = {
        employee.employee_id
        for employee in selected
    }

    assert selected_ids == {"E001", "E004"}


# ============================================================
# 3. GREEDY
# ============================================================

def test_greedy_algorithm():

    employees = create_test_employees()

    selected, total = greedy_employee_selection(
        employees,
        100000
    )

    # Greedy selects the lowest salaries first:
    # Vamsi = 30000
    # Akki = 40000
    # Total = 70000

    assert total == 70000

    selected_ids = {
        employee.employee_id
        for employee in selected
    }

    assert selected_ids == {"E004", "E002"}


# ============================================================
# 4. BACKTRACKING
# ============================================================

def test_backtracking():

    employees = create_test_employees()

    team = backtracking_team_selection(
        employees,
        2,
        100000
    )

    assert team is not None

    assert len(team) == 2

    total = sum(
        employee.salary
        for employee in team
    )

    assert total <= 100000


# ============================================================
# 5. BRANCH AND BOUND
# ============================================================

def test_branch_and_bound():

    employees = create_test_employees()

    selected, total = branch_and_bound_employee_selection(
        employees,
        100000
    )

    # Optimal combination:
    # Vaishnavi = 65000
    # Vamsi = 30000
    # Total = 95000

    assert total == 95000

    selected_ids = {
        employee.employee_id
        for employee in selected
    }

    assert selected_ids == {"E001", "E004"}