def merge_sort_employees(employees):
    """
    Divide and Conquer:
    Sort employees by salary using Merge Sort.
    """

    # Base case
    if len(employees) <= 1:
        return employees

    # Divide
    middle = len(employees) // 2

    left = employees[:middle]
    right = employees[middle:]

    # Conquer
    left = merge_sort_employees(left)
    right = merge_sort_employees(right)

    # Combine
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


def display_sorted_employees(employees):
    """
    Display employees sorted by salary.
    """

    sorted_employees = merge_sort_employees(employees)

    print("\n----- Employees Sorted by Salary -----")

    for employee in sorted_employees:
        print(employee)