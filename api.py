from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from main import Employee, EmployeeManager

from algorithm import (
    merge_sort_employees,
    maximum_salary_with_budget,
    greedy_employee_selection,
    backtracking_team_selection,
    branch_and_bound_employee_selection,
)


app = FastAPI(
    title="Employee Management System API"
)


# -------------------------------------------------
# CORS
# -------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------------------------------
# Employee Manager
# -------------------------------------------------

manager = EmployeeManager()


# -------------------------------------------------
# Employee Data Model
# -------------------------------------------------

class EmployeeData(BaseModel):
    id: str
    name: str
    email: str
    department: str
    salary: float


# -------------------------------------------------
# Helper Function
# -------------------------------------------------

def employee_to_dict(employee):
    return {
        "id": employee.employee_id,
        "name": employee.name,
        "email": employee.email,
        "department": employee.department,
        "salary": employee.salary,
    }


# -------------------------------------------------
# Home
# -------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "Employee Management System API is running"
    }


# -------------------------------------------------
# GET ALL EMPLOYEES
# -------------------------------------------------

@app.get("/employees")
def get_employees():

    return [
        employee_to_dict(employee)
        for employee in manager.employees.values()
    ]


# -------------------------------------------------
# ADD EMPLOYEE
# -------------------------------------------------

@app.post("/employees")
def add_employee(data: EmployeeData):

    employee = Employee(
        data.id,
        data.name,
        data.email,
        data.department,
        data.salary,
    )

    if not manager.add_employee(employee):

        raise HTTPException(
            status_code=400,
            detail="Employee ID already exists"
        )

    return {
        "message": "Employee added successfully",
        "employee": employee_to_dict(employee)
    }


# -------------------------------------------------
# UPDATE EMPLOYEE
# -------------------------------------------------

@app.put("/employees/{employee_id}")
def update_employee(
    employee_id: str,
    data: EmployeeData
):

    success = manager.update_employee(
        employee_id,
        data.name,
        data.email,
        data.department,
        data.salary,
    )

    if not success:

        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return {
        "message": "Employee updated successfully"
    }


# -------------------------------------------------
# DELETE EMPLOYEE
# -------------------------------------------------

@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: str):

    success = manager.delete_employee(employee_id)

    if not success:

        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return {
        "message": "Employee deleted successfully"
    }


# -------------------------------------------------
# SEARCH EMPLOYEE
# -------------------------------------------------

@app.get("/employees/search/{employee_id}")
def search_employee(employee_id: str):

    employee = manager.search_employee(employee_id)

    if employee is None:

        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return employee_to_dict(employee)


# =================================================
# ALGORITHM 1
# DIVIDE AND CONQUER - MERGE SORT
# =================================================

@app.get("/algorithms/merge-sort")
def merge_sort_algorithm():

    employees = list(
        manager.employees.values()
    )

    sorted_employees = merge_sort_employees(
        employees
    )

    return {
        "algorithm": "Divide and Conquer - Merge Sort",
        "complexity": "O(n log n)",
        "result": [
            employee_to_dict(employee)
            for employee in sorted_employees
        ]
    }


# =================================================
# ALGORITHM 2
# DYNAMIC PROGRAMMING
# =================================================

@app.get("/algorithms/dynamic-programming")
def dynamic_programming_algorithm(
    budget: float
):

    employees = list(
        manager.employees.values()
    )

    if not employees:

        return {
            "algorithm": "Dynamic Programming",
            "budget": budget,
            "total_salary": 0,
            "result": []
        }

    selected, total = maximum_salary_with_budget(
        employees,
        budget
    )

    return {
        "algorithm": "Dynamic Programming",
        "complexity": "O(n × budget)",
        "budget": budget,
        "total_salary": total,
        "result": [
            employee_to_dict(employee)
            for employee in selected
        ]
    }


# =================================================
# ALGORITHM 3
# GREEDY
# =================================================

@app.get("/algorithms/greedy")
def greedy_algorithm(
    budget: float
):

    employees = list(
        manager.employees.values()
    )

    if not employees:

        return {
            "algorithm": "Greedy",
            "budget": budget,
            "total_salary": 0,
            "result": []
        }

    selected, total = greedy_employee_selection(
        employees,
        budget
    )

    return {
        "algorithm": "Greedy",
        "complexity": "O(n log n)",
        "budget": budget,
        "total_salary": total,
        "result": [
            employee_to_dict(employee)
            for employee in selected
        ]
    }


# =================================================
# ALGORITHM 4
# BACKTRACKING
# =================================================

@app.get("/algorithms/backtracking")
def backtracking_algorithm(
    team_size: int,
    budget: float
):

    employees = list(
        manager.employees.values()
    )

    if not employees:

        return {
            "algorithm": "Backtracking",
            "team_size": team_size,
            "budget": budget,
            "total_salary": 0,
            "result": []
        }

    team = backtracking_team_selection(
        employees,
        team_size,
        budget
    )

    if team is None:

        return {
            "algorithm": "Backtracking",
            "team_size": team_size,
            "budget": budget,
            "total_salary": 0,
            "result": [],
            "message": "No suitable team found"
        }

    total = sum(
        employee.salary
        for employee in team
    )

    return {
        "algorithm": "Backtracking",
        "complexity": "O(2^n)",
        "team_size": team_size,
        "budget": budget,
        "total_salary": total,
        "result": [
            employee_to_dict(employee)
            for employee in team
        ]
    }


# =================================================
# ALGORITHM 5
# BRANCH AND BOUND
# =================================================

@app.get("/algorithms/branch-and-bound")
def branch_and_bound_algorithm(
    budget: float
):

    employees = list(
        manager.employees.values()
    )

    if not employees:

        return {
            "algorithm": "Branch and Bound",
            "budget": budget,
            "total_salary": 0,
            "result": []
        }

    selected, total = (
        branch_and_bound_employee_selection(
            employees,
            budget
        )
    )

    return {
        "algorithm": "Branch and Bound",
        "complexity": "Exponential worst case",
        "budget": budget,
        "total_salary": total,
        "result": [
            employee_to_dict(employee)
            for employee in selected
        ]
    }