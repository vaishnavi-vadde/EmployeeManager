import { useEffect, useState } from "react";
import "./App.css";

interface Employee {
  id: string;
  name: string;
  email: string;
  department: string;
  salary: number;
}

interface AlgorithmResponse {
  algorithm: string;
  complexity?: string;
  budget?: number;
  team_size?: number;
  total_salary?: number;
  result: Employee[];
  message?: string;
}

const API_URL = "http://127.0.0.1:8000/employees";
const ALGORITHM_API = "http://127.0.0.1:8000/algorithms";

function App() {
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [search, setSearch] = useState("");
  const [department, setDepartment] = useState("");
  const [editingId, setEditingId] = useState<string | null>(null);

  // Employee form
  const [form, setForm] = useState<Employee>({
    id: "",
    name: "",
    email: "",
    department: "",
    salary: 0,
  });

  // Algorithm states
  const [selectedAlgorithm, setSelectedAlgorithm] =
    useState("merge-sort");

  const [budget, setBudget] = useState<number>(100000);

  const [teamSize, setTeamSize] = useState<number>(2);

  const [algorithmResult, setAlgorithmResult] =
    useState<AlgorithmResponse | null>(null);

  const [algorithmLoading, setAlgorithmLoading] =
    useState(false);

  // ------------------------------------------------
  // FETCH EMPLOYEES
  // ------------------------------------------------

  useEffect(() => {
    fetchEmployees();
  }, []);

  const fetchEmployees = async () => {
    try {
      const response = await fetch(API_URL);

      if (!response.ok) {
        throw new Error("Failed to fetch employees");
      }

      const data = await response.json();

      setEmployees(data);
    } catch (error) {
      console.error(error);
      alert("Cannot connect to Python backend.");
    }
  };

  // ------------------------------------------------
  // CLEAR FORM
  // ------------------------------------------------

  const clearForm = () => {
    setForm({
      id: "",
      name: "",
      email: "",
      department: "",
      salary: 0,
    });

    setEditingId(null);
  };

  // ------------------------------------------------
  // START EDIT
  // ------------------------------------------------

  const startEdit = (employee: Employee) => {
    setForm(employee);

    setEditingId(employee.id);

    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  };

  // ------------------------------------------------
  // ADD EMPLOYEE
  // ------------------------------------------------

  const addEmployee = async () => {
    if (
      !form.id ||
      !form.name ||
      !form.email ||
      !form.department ||
      !form.salary
    ) {
      alert("Please fill all fields");

      return;
    }

    try {
      const response = await fetch(API_URL, {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
        },

        body: JSON.stringify(form),
      });

      const data = await response.json();

      if (!response.ok) {
        alert(
          data.detail ||
            "Failed to add employee"
        );

        return;
      }

      alert("Employee added successfully!");

      clearForm();

      fetchEmployees();
    } catch (error) {
      console.error(error);

      alert(
        "Cannot connect to Python backend."
      );
    }
  };

  // ------------------------------------------------
  // UPDATE EMPLOYEE
  // ------------------------------------------------

  const updateEmployee = async () => {
    if (!editingId) {
      return;
    }

    if (
      !form.name ||
      !form.email ||
      !form.department ||
      !form.salary
    ) {
      alert("Please fill all fields");

      return;
    }

    try {
      const response = await fetch(
        `${API_URL}/${editingId}`,
        {
          method: "PUT",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify(form),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        alert(
          data.detail ||
            "Failed to update employee"
        );

        return;
      }

      alert(
        "Employee updated successfully!"
      );

      clearForm();

      fetchEmployees();
    } catch (error) {
      console.error(error);

      alert(
        "Cannot connect to Python backend."
      );
    }
  };

  // ------------------------------------------------
  // DELETE EMPLOYEE
  // ------------------------------------------------

  const deleteEmployee = async (
    id: string
  ) => {
    try {
      const response = await fetch(
        `${API_URL}/${id}`,
        {
          method: "DELETE",
        }
      );

      const data = await response.json();

      if (!response.ok) {
        alert(
          data.detail ||
            "Failed to delete employee"
        );

        return;
      }

      alert(
        "Employee deleted successfully!"
      );

      fetchEmployees();
    } catch (error) {
      console.error(error);

      alert(
        "Cannot connect to Python backend."
      );
    }
  };

  // ------------------------------------------------
  // SEARCH + DEPARTMENT FILTER
  // ------------------------------------------------

  const filteredEmployees =
    employees.filter((employee) => {
      const matchesSearch =
        employee.id
          .toLowerCase()
          .includes(search.toLowerCase()) ||
        employee.name
          .toLowerCase()
          .includes(search.toLowerCase()) ||
        employee.email
          .toLowerCase()
          .includes(search.toLowerCase()) ||
        employee.department
          .toLowerCase()
          .includes(search.toLowerCase());

      const matchesDepartment =
        department === "" ||
        employee.department
          .toLowerCase() ===
          department.toLowerCase();

      return (
        matchesSearch &&
        matchesDepartment
      );
    });

  // ------------------------------------------------
  // AVERAGE SALARY
  // ------------------------------------------------

  const averageSalary =
    employees.length > 0
      ? employees.reduce(
          (total, employee) =>
            total + employee.salary,
          0
        ) / employees.length
      : 0;

  // ------------------------------------------------
  // DEPARTMENTS
  // ------------------------------------------------

  const departments = [
    ...new Set(
      employees.map(
        (employee) =>
          employee.department
      )
    ),
  ];

  // =================================================
  // RUN ALGORITHM
  // =================================================

  const runAlgorithm = async () => {
    setAlgorithmLoading(true);

    setAlgorithmResult(null);

    try {
      let url = "";

      // ---------------------------------------------
      // MERGE SORT
      // ---------------------------------------------

      if (
        selectedAlgorithm ===
        "merge-sort"
      ) {
        url = `${ALGORITHM_API}/merge-sort`;
      }

      // ---------------------------------------------
      // DYNAMIC PROGRAMMING
      // ---------------------------------------------

      else if (
        selectedAlgorithm ===
        "dynamic-programming"
      ) {
        url =
          `${ALGORITHM_API}/dynamic-programming` +
          `?budget=${budget}`;
      }

      // ---------------------------------------------
      // GREEDY
      // ---------------------------------------------

      else if (
        selectedAlgorithm ===
        "greedy"
      ) {
        url =
          `${ALGORITHM_API}/greedy` +
          `?budget=${budget}`;
      }

      // ---------------------------------------------
      // BACKTRACKING
      // ---------------------------------------------

      else if (
        selectedAlgorithm ===
        "backtracking"
      ) {
        url =
          `${ALGORITHM_API}/backtracking` +
          `?team_size=${teamSize}` +
          `&budget=${budget}`;
      }

      // ---------------------------------------------
      // BRANCH AND BOUND
      // ---------------------------------------------

      else if (
        selectedAlgorithm ===
        "branch-and-bound"
      ) {
        url =
          `${ALGORITHM_API}/branch-and-bound` +
          `?budget=${budget}`;
      }

      const response = await fetch(url);

      const data =
        await response.json();

      if (!response.ok) {
        alert(
          data.detail ||
            "Algorithm execution failed."
        );

        return;
      }

      setAlgorithmResult(data);
    } catch (error) {
      console.error(error);

      alert(
        "Cannot connect to Python backend."
      );
    } finally {
      setAlgorithmLoading(false);
    }
  };

  // =================================================
  // MAIN UI
  // =================================================

  return (
    <div className="container">

      <h1>
        Employee Management System
      </h1>

      {/* ============================================
          STATISTICS
      ============================================ */}

      <div className="stats">

        <div className="stat-card">
          <h3>Total Employees</h3>

          <p>
            {employees.length}
          </p>
        </div>

        <div className="stat-card">
          <h3>Average Salary</h3>

          <p>
            ₹{averageSalary.toFixed(2)}
          </p>
        </div>

        <div className="stat-card">
          <h3>Departments</h3>

          <p>
            {departments.length}
          </p>
        </div>

      </div>

      {/* ============================================
          ADD / EDIT EMPLOYEE
      ============================================ */}

      <div className="form-card">

        <h2>
          {editingId
            ? "Edit Employee"
            : "Add Employee"}
        </h2>

        <div className="form-grid">

          <input
            type="text"
            placeholder="Employee ID"
            value={form.id}
            disabled={
              editingId !== null
            }
            onChange={(e) =>
              setForm({
                ...form,
                id: e.target.value,
              })
            }
          />

          <input
            type="text"
            placeholder="Name"
            value={form.name}
            onChange={(e) =>
              setForm({
                ...form,
                name: e.target.value,
              })
            }
          />

          <input
            type="email"
            placeholder="Email"
            value={form.email}
            onChange={(e) =>
              setForm({
                ...form,
                email: e.target.value,
              })
            }
          />

          <input
            type="text"
            placeholder="Department"
            value={form.department}
            onChange={(e) =>
              setForm({
                ...form,
                department:
                  e.target.value,
              })
            }
          />

          <input
            type="text"
            placeholder="Salary"
            value={
              form.salary === 0
                ? ""
                : form.salary
            }
            onChange={(e) =>
              setForm({
                ...form,
                salary:
                  Number(
                    e.target.value
                  ) || 0,
              })
            }
          />

        </div>

        {editingId ? (

          <div>

            <button
              onClick={
                updateEmployee
              }
            >
              Update Employee
            </button>

            <button
              className="cancel-btn"
              onClick={
                clearForm
              }
            >
              Cancel
            </button>

          </div>

        ) : (

          <button
            onClick={
              addEmployee
            }
          >
            Add Employee
          </button>

        )}

      </div>

      {/* ============================================
          EMPLOYEE LIST
      ============================================ */}

      <div className="list-card">

        <div className="list-header">

          <h2>
            Employee List
          </h2>

          <div className="filters">

            <input
              className="search"
              type="text"
              placeholder="Search employee..."
              value={search}
              onChange={(e) =>
                setSearch(
                  e.target.value
                )
              }
            />

            <select
              value={department}
              onChange={(e) =>
                setDepartment(
                  e.target.value
                )
              }
            >

              <option value="">
                All Departments
              </option>

              {departments.map(
                (dept) => (
                  <option
                    key={dept}
                    value={dept}
                  >
                    {dept}
                  </option>
                )
              )}

            </select>

          </div>

        </div>

        {filteredEmployees.length ===
        0 ? (

          <p className="empty">
            No employees found.
          </p>

        ) : (

          <table>

            <thead>

              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Email</th>
                <th>Department</th>
                <th>Salary</th>
                <th>Action</th>
              </tr>

            </thead>

            <tbody>

              {filteredEmployees.map(
                (employee) => (

                  <tr
                    key={
                      employee.id
                    }
                  >

                    <td>
                      {employee.id}
                    </td>

                    <td>
                      {employee.name}
                    </td>

                    <td>
                      {employee.email}
                    </td>

                    <td>
                      {
                        employee.department
                      }
                    </td>

                    <td>
                      ₹
                      {
                        employee.salary
                      }
                    </td>

                    <td>

                      <button
                        className="edit-btn"
                        onClick={() =>
                          startEdit(
                            employee
                          )
                        }
                      >
                        Edit
                      </button>

                      <button
                        className="delete-btn"
                        onClick={() =>
                          deleteEmployee(
                            employee.id
                          )
                        }
                      >
                        Delete
                      </button>

                    </td>

                  </tr>

                )
              )}

            </tbody>

          </table>

        )}

      </div>

      {/* ============================================
          ALGORITHM DEMONSTRATION
      ============================================ */}

      <div className="algorithm-card">

        <h2>
          Algorithm Demonstration
        </h2>

        <p className="algorithm-description">
          Demonstrate the five algorithm
          design techniques used in the
          Employee Management System.
        </p>

        {/* Algorithm Selection */}

        <div className="algorithm-controls">

          <label>
            Select Algorithm
          </label>

          <select
            value={
              selectedAlgorithm
            }
            onChange={(e) => {
              setSelectedAlgorithm(
                e.target.value
              );

              setAlgorithmResult(
                null
              );
            }}
          >

            <option value="merge-sort">
              Divide & Conquer -
              Merge Sort
            </option>

            <option value="dynamic-programming">
              Dynamic Programming
            </option>

            <option value="greedy">
              Greedy
            </option>

            <option value="backtracking">
              Backtracking
            </option>

            <option value="branch-and-bound">
              Branch & Bound
            </option>

          </select>

        </div>

        {/* Budget */}

        {selectedAlgorithm !==
          "merge-sort" && (

          <div className="algorithm-input">

            <label>
              Salary Budget
            </label>

            <input
              type="number"
              value={budget}
              onChange={(e) =>
                setBudget(
                  Number(
                    e.target.value
                  )
                )
              }
            />

          </div>

        )}

        {/* Team Size */}

        {selectedAlgorithm ===
          "backtracking" && (

          <div className="algorithm-input">

            <label>
              Required Team Size
            </label>

            <input
              type="number"
              min="1"
              value={teamSize}
              onChange={(e) =>
                setTeamSize(
                  Number(
                    e.target.value
                  )
                )
              }
            />

          </div>

        )}

        {/* Run Button */}

        <button
          className="run-algorithm-btn"
          onClick={
            runAlgorithm
          }
          disabled={
            algorithmLoading
          }
        >

          {algorithmLoading
            ? "Running..."
            : "Run Algorithm"}

        </button>

        {/* =========================================
            ALGORITHM RESULT
        ========================================= */}

        {algorithmResult && (

          <div className="algorithm-result">

            <h3>
              {algorithmResult.algorithm}
            </h3>

            {algorithmResult.complexity && (

              <p>
                <strong>
                  Time Complexity:
                </strong>{" "}
                {
                  algorithmResult.complexity
                }
              </p>

            )}

            {algorithmResult.budget !==
              undefined && (

              <p>
                <strong>
                  Budget:
                </strong>{" "}
                ₹
                {
                  algorithmResult.budget
                }
              </p>

            )}

            {algorithmResult.team_size !==
              undefined && (

              <p>
                <strong>
                  Team Size:
                </strong>{" "}
                {
                  algorithmResult.team_size
                }
              </p>

            )}

            {algorithmResult.total_salary !==
              undefined && (

              <p>
                <strong>
                  Total Salary:
                </strong>{" "}
                ₹
                {
                  algorithmResult.total_salary
                }
              </p>

            )}

            {algorithmResult.message && (

              <p className="algorithm-message">
                {
                  algorithmResult.message
                }
              </p>

            )}

            {algorithmResult.result.length >
              0 && (

              <table>

                <thead>

                  <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Department</th>
                    <th>Salary</th>
                  </tr>

                </thead>

                <tbody>

                  {algorithmResult.result.map(
                    (employee) => (

                      <tr
                        key={
                          employee.id
                        }
                      >

                        <td>
                          {
                            employee.id
                          }
                        </td>

                        <td>
                          {
                            employee.name
                          }
                        </td>

                        <td>
                          {
                            employee.email
                          }
                        </td>

                        <td>
                          {
                            employee.department
                          }
                        </td>

                        <td>
                          ₹
                          {
                            employee.salary
                          }
                        </td>

                      </tr>

                    )
                  )}

                </tbody>

              </table>

            )}

          </div>

        )}

      </div>

    </div>
  );
}

export default App;