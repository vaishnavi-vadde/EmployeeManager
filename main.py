class Employee:
    def __init__(self, employee_id, name, email, department, salary):
        self.employee_id = employee_id
        self.name = name
        self.email = email
        self.department = department
        self.salary = salary

    def __str__(self):
        return (
            f"ID: {self.employee_id} | "
            f"Name: {self.name} | "
            f"Email: {self.email} | "
            f"Department: {self.department} | "
            f"Salary: {self.salary}"
        )


class EmployeeManager:
    def __init__(self):
        self.employees = {}

    def add_employee(self, employee):
        if employee.employee_id in self.employees:
            print("Employee ID already exists.")
            return False

        self.employees[employee.employee_id] = employee
        print("Employee added successfully.")
        return True

    def view_employees(self):
        if not self.employees:
            print("No employees found.")
            return

        print("\n----- Employee List -----")

        for employee in self.employees.values():
            print(employee)

    def search_employee(self, employee_id):
        return self.employees.get(employee_id)

    def update_employee(
        self,
        employee_id,
        name,
        email,
        department,
        salary
    ):
        employee = self.employees.get(employee_id)

        if employee is None:
            print("Employee not found.")
            return False

        employee.name = name
        employee.email = email
        employee.department = department
        employee.salary = salary

        print("Employee updated successfully.")
        return True

    def delete_employee(self, employee_id):
        if employee_id not in self.employees:
            print("Employee not found.")
            return False

        del self.employees[employee_id]

        print("Employee deleted successfully.")
        return True

    def employees_by_department(self, department):
        result = []

        for employee in self.employees.values():
            if employee.department.lower() == department.lower():
                result.append(employee)

        return result


def calculate_average_salary(employees):
    employees = list(employees)

    if not employees:
        return 0

    total_salary = sum(
        employee.salary
        for employee in employees
    )

    return total_salary / len(employees)


# ============================================================
# ALGORITHM DEMONSTRATION
# ============================================================

def algorithm_demo_menu(manager):

    from algorithm import (
        merge_sort_employees,
        maximum_salary_with_budget,
        greedy_employee_selection,
        backtracking_team_selection,
        branch_and_bound_employee_selection,
    )

    employees = list(manager.employees.values())

    if not employees:
        print("\nNo employees available.")
        return

    while True:

        print("\n===== Algorithm Demonstration =====")
        print("1. Divide and Conquer - Merge Sort")
        print("2. Dynamic Programming")
        print("3. Greedy")
        print("4. Backtracking")
        print("5. Branch and Bound")
        print("6. Back to Main Menu")

        choice = input("Enter your choice: ").strip()

        # ----------------------------------------------------
        # 1. DIVIDE AND CONQUER
        # ----------------------------------------------------

        if choice == "1":

            sorted_employees = merge_sort_employees(
                employees
            )

            print(
                "\n--- Divide and Conquer: Merge Sort ---"
            )

            print("Employees sorted by salary:")

            for employee in sorted_employees:
                print(employee)

        # ----------------------------------------------------
        # 2. DYNAMIC PROGRAMMING
        # ----------------------------------------------------

        elif choice == "2":

            try:
                budget = float(
                    input("Enter salary budget: ")
                )
            except ValueError:
                print("Invalid budget.")
                continue

            selected, total = maximum_salary_with_budget(
                employees,
                budget
            )

            print("\n--- Dynamic Programming ---")
            print(f"Budget: {budget:.2f}")
            print(
                f"Maximum Salary Used: {total:.2f}"
            )

            print("Selected employees:")

            for employee in selected:
                print(employee)

        # ----------------------------------------------------
        # 3. GREEDY
        # ----------------------------------------------------

        elif choice == "3":

            try:
                budget = float(
                    input("Enter salary budget: ")
                )
            except ValueError:
                print("Invalid budget.")
                continue

            selected, total = greedy_employee_selection(
                employees,
                budget
            )

            print("\n--- Greedy Algorithm ---")
            print(f"Budget: {budget:.2f}")
            print(f"Total Salary: {total:.2f}")

            print("Selected employees:")

            for employee in selected:
                print(employee)

        # ----------------------------------------------------
        # 4. BACKTRACKING
        # ----------------------------------------------------

        elif choice == "4":

            try:
                team_size = int(
                    input("Enter required team size: ")
                )

                budget = float(
                    input("Enter salary budget: ")
                )

            except ValueError:
                print("Invalid input.")
                continue

            team = backtracking_team_selection(
                employees,
                team_size,
                budget
            )

            print("\n--- Backtracking ---")

            if team is None:

                print(
                    "No suitable team found "
                    "within the budget."
                )

            else:

                total = sum(
                    employee.salary
                    for employee in team
                )

                print(f"Team Size: {team_size}")
                print(f"Budget: {budget:.2f}")
                print(f"Total Salary: {total:.2f}")

                print("Selected team:")

                for employee in team:
                    print(employee)

        # ----------------------------------------------------
        # 5. BRANCH AND BOUND
        # ----------------------------------------------------

        elif choice == "5":

            try:
                budget = float(
                    input("Enter salary budget: ")
                )

            except ValueError:
                print("Invalid budget.")
                continue

            selected, total = (
                branch_and_bound_employee_selection(
                    employees,
                    budget
                )
            )

            print("\n--- Branch and Bound ---")
            print(f"Budget: {budget:.2f}")
            print(
                f"Maximum Salary Used: {total:.2f}"
            )

            print("Selected employees:")

            for employee in selected:
                print(employee)

        # ----------------------------------------------------
        # 6. BACK TO MAIN MENU
        # ----------------------------------------------------

        elif choice == "6":

            break

        else:

            print(
                "Invalid choice. Please try again."
            )


# ============================================================
# MAIN MENU
# ============================================================

def display_menu():

    print("\n===== Employee Management System =====")

    print("1. Add Employee")
    print("2. View Employees")
    print("3. Search Employee")
    print("4. Update Employee")
    print("5. Delete Employee")
    print("6. Average Salary")
    print("7. Employees by Department")
    print("8. Algorithm Demonstration")
    print("9. Exit")


# ============================================================
# ADD EMPLOYEE
# ============================================================

def add_employee_menu(manager):

    print("\n----- Add Employee -----")

    employee_id = input(
        "Enter Employee ID: "
    ).strip()

    name = input(
        "Enter Name: "
    ).strip()

    email = input(
        "Enter Email: "
    ).strip()

    department = input(
        "Enter Department: "
    ).strip()

    try:

        salary = float(
            input("Enter Salary: ")
        )

    except ValueError:

        print("Invalid salary.")
        return

    employee = Employee(
        employee_id,
        name,
        email,
        department,
        salary
    )

    manager.add_employee(employee)


# ============================================================
# SEARCH EMPLOYEE
# ============================================================

def search_employee_menu(manager):

    print("\n----- Search Employee -----")

    employee_id = input(
        "Enter Employee ID: "
    ).strip()

    employee = manager.search_employee(
        employee_id
    )

    if employee:

        print("\nEmployee Found:")
        print(employee)

    else:

        print("Employee not found.")


# ============================================================
# UPDATE EMPLOYEE
# ============================================================

def update_employee_menu(manager):

    print("\n----- Update Employee -----")

    employee_id = input(
        "Enter Employee ID: "
    ).strip()

    if employee_id not in manager.employees:

        print("Employee not found.")
        return

    name = input(
        "Enter New Name: "
    ).strip()

    email = input(
        "Enter New Email: "
    ).strip()

    department = input(
        "Enter New Department: "
    ).strip()

    try:

        salary = float(
            input("Enter New Salary: ")
        )

    except ValueError:

        print("Invalid salary.")
        return

    manager.update_employee(
        employee_id,
        name,
        email,
        department,
        salary
    )


# ============================================================
# DELETE EMPLOYEE
# ============================================================

def delete_employee_menu(manager):

    print("\n----- Delete Employee -----")

    employee_id = input(
        "Enter Employee ID: "
    ).strip()

    manager.delete_employee(
        employee_id
    )


# ============================================================
# AVERAGE SALARY
# ============================================================

def average_salary_menu(manager):

    print("\n----- Average Salary -----")

    average = calculate_average_salary(
        manager.employees.values()
    )

    print(
        f"Average Salary: {average:.2f}"
    )


# ============================================================
# DEPARTMENT
# ============================================================

def department_menu(manager):

    print(
        "\n----- Employees by Department -----"
    )

    department = input(
        "Enter Department: "
    ).strip()

    employees = manager.employees_by_department(
        department
    )

    if not employees:

        print(
            "No employees found in this department."
        )

        return

    print(
        f"\nEmployees in {department}:"
    )

    for employee in employees:

        print(employee)


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():

    manager = EmployeeManager()

    while True:

        display_menu()

        choice = input(
            "Enter your choice: "
        ).strip()

        if choice == "1":

            add_employee_menu(manager)

        elif choice == "2":

            manager.view_employees()

        elif choice == "3":

            search_employee_menu(manager)

        elif choice == "4":

            update_employee_menu(manager)

        elif choice == "5":

            delete_employee_menu(manager)

        elif choice == "6":

            average_salary_menu(manager)

        elif choice == "7":

            department_menu(manager)

        elif choice == "8":

            algorithm_demo_menu(manager)

        elif choice == "9":

            print(
                "Thank you for using "
                "Employee Management System."
            )

            break

        else:

            print(
                "Invalid choice. Please try again."
            )


if __name__ == "__main__":
    main()