import time

from main import Employee
from algorithm import merge_sort_employees


def create_employees(count):
    employees = []

    for i in range(count):
        employees.append(
            Employee(
                f"E{i}",
                f"Employee{i}",
                f"employee{i}@gmail.com",
                "IT",
                30000 + (i % 100) * 1000
            )
        )

    return employees


def measure_merge_sort(employees):
    start_time = time.perf_counter()

    merge_sort_employees(employees)

    end_time = time.perf_counter()

    return end_time - start_time


def measure_linear_search(employees):
    target_id = employees[-1].employee_id

    start_time = time.perf_counter()

    for employee in employees:
        if employee.employee_id == target_id:
            break

    end_time = time.perf_counter()

    return end_time - start_time


def measure_dictionary_lookup(employees):
    employee_dictionary = {
        employee.employee_id: employee
        for employee in employees
    }

    target_id = employees[-1].employee_id

    start_time = time.perf_counter()

    employee_dictionary.get(target_id)

    end_time = time.perf_counter()

    return end_time - start_time


def main():
    sizes = [100, 1000, 5000]

    print("----- Performance Evaluation -----")

    for size in sizes:
        employees = create_employees(size)

        merge_sort_time = measure_merge_sort(employees)
        linear_search_time = measure_linear_search(employees)
        dictionary_time = measure_dictionary_lookup(employees)

        print(f"\nEmployees: {size}")
        print(f"Merge Sort Time: {merge_sort_time:.6f} seconds")
        print(f"Linear Search Time: {linear_search_time:.6f} seconds")
        print(f"Dictionary Lookup Time: {dictionary_time:.6f} seconds")


if __name__ == "__main__":
    main()
    