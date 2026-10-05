from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from main import Employee, EmployeeManager


app = FastAPI(title="Employee Management System API")


# Allow React frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


manager = EmployeeManager()


class EmployeeData(BaseModel):
    id: str
    name: str
    email: str
    department: str
    salary: float


@app.get("/")
def home():
    return {"message": "Employee Management System API is running"}


@app.get("/employees")
def get_employees():
    return [
        {
            "id": employee.employee_id,
            "name": employee.name,
            "email": employee.email,
            "department": employee.department,
            "salary": employee.salary,
        }
        for employee in manager.employees.values()
    ]


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
        "employee": {
            "id": employee.employee_id,
            "name": employee.name,
            "email": employee.email,
            "department": employee.department,
            "salary": employee.salary,
        },
    }


@app.put("/employees/{employee_id}")
def update_employee(employee_id: str, data: EmployeeData):

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

    return {"message": "Employee updated successfully"}


@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: str):

    success = manager.delete_employee(employee_id)

    if not success:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return {"message": "Employee deleted successfully"}


@app.get("/employees/search/{employee_id}")
def search_employee(employee_id: str):

    employee = manager.search_employee(employee_id)

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return {
        "id": employee.employee_id,
        "name": employee.name,
        "email": employee.email,
        "department": employee.department,
        "salary": employee.salary,
    }