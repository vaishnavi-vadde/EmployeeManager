from main import Employee


# ============================================================
# 1. DIVIDE AND CONQUER
# ============================================================

def merge_sort_employees(employees):
    """
    Divide and Conquer:
    Sort employees by salary using Merge Sort.
    """

    if len(employees) <= 1:
        return employees

    middle = len(employees) // 2

    left = employees[:middle]
    right = employees[middle:]

    left = merge_sort_employees(left)
    right = merge_sort_employees(right)

    return merge(left, right)


def merge(left, right):
    """
    Merge two sorted employee lists.
    """

    result = []

    i = 0
    j = 0

    while i < len(left) and j < len(right):

        if left[i].salary <= right[j].salary:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])

    return result


# ============================================================
# 2. DYNAMIC PROGRAMMING
# ============================================================

def maximum_salary_with_budget(employees, budget):
    """
    Dynamic Programming:
    Find the maximum total salary that can be selected
    without exceeding the given budget.

    Returns:
        selected employees
        total salary
    """

    budget = int(budget)

    dp = [0] * (budget + 1)

    selected = [[] for _ in range(budget + 1)]

    for employee in employees:

        salary = int(employee.salary)

        for current_budget in range(budget, salary - 1, -1):

            new_salary = dp[current_budget - salary] + salary

            if new_salary > dp[current_budget]:

                dp[current_budget] = new_salary

                selected[current_budget] = (
                    selected[current_budget - salary]
                    + [employee]
                )

    return selected[budget], dp[budget]


# ============================================================
# 3. GREEDY
# ============================================================

def greedy_employee_selection(employees, budget):
    """
    Greedy Algorithm:
    Select employees with the lowest salaries first
    while staying within the budget.

    Goal:
    Select the maximum number of employees
    using the available budget.
    """

    sorted_employees = sorted(
        employees,
        key=lambda employee: employee.salary
    )

    selected = []
    total_salary = 0

    for employee in sorted_employees:

        if total_salary + employee.salary <= budget:

            selected.append(employee)
            total_salary += employee.salary

        else:
            break

    return selected, total_salary


# ============================================================
# 4. BACKTRACKING
# ============================================================

def backtracking_team_selection(employees, team_size, budget):
    """
    Backtracking:
    Find a team containing exactly team_size employees
    whose total salary does not exceed the budget.

    Returns:
        selected team or None
    """

    result = []

    def backtrack(index, team, total_salary):

        if len(team) == team_size:

            if total_salary <= budget:
                result.extend(team)
                return True

            return False

        if index >= len(employees):
            return False

        remaining = len(employees) - index

        if len(team) + remaining < team_size:
            return False

        employee = employees[index]

        # Choose current employee
        if total_salary + employee.salary <= budget:

            if backtrack(
                index + 1,
                team + [employee],
                total_salary + employee.salary
            ):
                return True

        # Do not choose current employee
        if backtrack(
            index + 1,
            team,
            total_salary
        ):
            return True

        return False

    found = backtrack(0, [], 0)

    if found:
        return result

    return None


# ============================================================
# 5. BRANCH AND BOUND
# ============================================================

def branch_and_bound_employee_selection(employees, budget):
    """
    Branch and Bound:
    Find a combination of employees whose total salary
    is as close as possible to the budget without exceeding it.

    The algorithm explores include/exclude branches and
    prunes branches that cannot improve the current solution.

    Returns:
        selected employees
        total salary
    """

    employees = sorted(
        employees,
        key=lambda employee: employee.salary,
        reverse=True
    )

    best_selection = []
    best_salary = 0

    def upper_bound(index, current_salary):
        """
        Calculate an optimistic upper bound.
        """

        total = current_salary

        for i in range(index, len(employees)):

            if total + employees[i].salary <= budget:
                total += employees[i].salary

        return total

    def branch(index, current_selection, current_salary):

        nonlocal best_selection
        nonlocal best_salary

        if current_salary > budget:
            return

        if current_salary > best_salary:

            best_salary = current_salary
            best_selection = current_selection.copy()

        if index >= len(employees):
            return

        bound = upper_bound(
            index,
            current_salary
        )

        if bound <= best_salary:
            return

        employee = employees[index]

        # Branch 1: include employee
        if current_salary + employee.salary <= budget:

            branch(
                index + 1,
                current_selection + [employee],
                current_salary + employee.salary
            )

        # Branch 2: exclude employee
        branch(
            index + 1,
            current_selection,
            current_salary
        )

    branch(0, [], 0)

    return best_selection, best_salary


# ============================================================
# DISPLAY FUNCTIONS
# ============================================================

def display_sorted_employees(employees):
    """
    Display employees sorted by salary.
    """

    sorted_employees = merge_sort_employees(employees)

    print("\n----- Employees Sorted by Salary -----")

    for employee in sorted_employees:
        print(employee)


def display_dp_selection(employees, budget):
    """
    Display Dynamic Programming result.
    """

    selected, total = maximum_salary_with_budget(
        employees,
        budget
    )

    print("\n----- Dynamic Programming -----")
    print(f"Budget: {budget}")
    print(f"Maximum Salary Used: {total}")

    for employee in selected:
        print(employee)


def display_greedy_selection(employees, budget):
    """
    Display Greedy result.
    """

    selected, total = greedy_employee_selection(
        employees,
        budget
    )

    print("\n----- Greedy Algorithm -----")
    print(f"Budget: {budget}")
    print(f"Total Salary: {total}")

    for employee in selected:
        print(employee)


def display_backtracking_team(employees, team_size, budget):
    """
    Display Backtracking result.
    """

    team = backtracking_team_selection(
        employees,
        team_size,
        budget
    )

    print("\n----- Backtracking -----")

    if team is None:
        print("No suitable team found.")
        return

    total = sum(employee.salary for employee in team)

    print(f"Team Size: {team_size}")
    print(f"Budget: {budget}")
    print(f"Total Salary: {total}")

    for employee in team:
        print(employee)


def display_branch_and_bound(employees, budget):
    """
    Display Branch and Bound result.
    """

    selected, total = branch_and_bound_employee_selection(
        employees,
        budget
    )

    print("\n----- Branch and Bound -----")
    print(f"Budget: {budget}")
    print(f"Maximum Salary Used: {total}")

    for employee in selected:
        print(employee)