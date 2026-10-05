import { useEffect, useState } from "react";
import "./App.css";

interface Employee {
  id: string;
  name: string;
  email: string;
  department: string;
  salary: number;
}

const API_URL = "http://127.0.0.1:8000/employees";

function App() {
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [search, setSearch] = useState("");
  const [department, setDepartment] = useState("");
  const [editingId, setEditingId] = useState<string | null>(null);

  const [form, setForm] = useState<Employee>({
    id: "",
    name: "",
    email: "",
    department: "",
    salary: 0,
  });

  useEffect(() => {
    fetchEmployees();
  }, []);

  const fetchEmployees = async () => {
    try {
      const response = await fetch(API_URL);
      const data = await response.json();
      setEmployees(data);
    } catch (error) {
      console.error(error);
      alert("Cannot connect to Python backend.");
    }
  };

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

  const startEdit = (employee: Employee) => {
    setForm(employee);
    setEditingId(employee.id);

    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  };

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
        alert(data.detail || "Failed to add employee");
        return;
      }

      alert("Employee added successfully!");

      clearForm();
      fetchEmployees();
    } catch (error) {
      console.error(error);
      alert("Cannot connect to Python backend.");
    }
  };

  const updateEmployee = async () => {
    if (!editingId) return;

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
        alert(data.detail || "Failed to update employee");
        return;
      }

      alert("Employee updated successfully!");

      clearForm();
      fetchEmployees();
    } catch (error) {
      console.error(error);
      alert("Cannot connect to Python backend.");
    }
  };

  const deleteEmployee = async (id: string) => {
    try {
      const response = await fetch(
        `${API_URL}/${id}`,
        {
          method: "DELETE",
        }
      );

      const data = await response.json();

      if (!response.ok) {
        alert(data.detail || "Failed to delete employee");
        return;
      }

      alert("Employee deleted successfully!");

      fetchEmployees();
    } catch (error) {
      console.error(error);
      alert("Cannot connect to Python backend.");
    }
  };

  // Search + Department Filter
  const filteredEmployees = employees.filter((employee) => {
    const matchesSearch =
      employee.id.toLowerCase().includes(search.toLowerCase()) ||
      employee.name.toLowerCase().includes(search.toLowerCase()) ||
      employee.email.toLowerCase().includes(search.toLowerCase()) ||
      employee.department.toLowerCase().includes(search.toLowerCase());

    const matchesDepartment =
      department === "" ||
      employee.department.toLowerCase() ===
        department.toLowerCase();

    return matchesSearch && matchesDepartment;
  });

  // Average salary
  const averageSalary =
    employees.length > 0
      ? employees.reduce(
          (total, employee) => total + employee.salary,
          0
        ) / employees.length
      : 0;

  // Departments
  const departments = [
    ...new Set(employees.map((employee) => employee.department)),
  ];

  return (
    <div className="container">

      <h1>Employee Management System</h1>

      {/* Statistics */}
      <div className="stats">
        <div className="stat-card">
          <h3>Total Employees</h3>
          <p>{employees.length}</p>
        </div>

        <div className="stat-card">
          <h3>Average Salary</h3>
          <p>₹{averageSalary.toFixed(2)}</p>
        </div>

        <div className="stat-card">
          <h3>Departments</h3>
          <p>{departments.length}</p>
        </div>
      </div>

      {/* Add / Edit */}
      <div className="form-card">

        <h2>
          {editingId ? "Edit Employee" : "Add Employee"}
        </h2>

        <div className="form-grid">

          <input
            type="text"
            placeholder="Employee ID"
            value={form.id}
            disabled={editingId !== null}
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
                department: e.target.value,
              })
            }
          />

          <input
            type="text"
            placeholder="Salary"
            value={form.salary === 0 ? "" : form.salary}
            onChange={(e) =>
              setForm({
                ...form,
                salary: Number(e.target.value) || 0,
              })
            }
          />

        </div>

        {editingId ? (
          <div>
            <button onClick={updateEmployee}>
              Update Employee
            </button>

            <button
              className="cancel-btn"
              onClick={clearForm}
            >
              Cancel
            </button>
          </div>
        ) : (
          <button onClick={addEmployee}>
            Add Employee
          </button>
        )}

      </div>

      {/* Employee List */}
      <div className="list-card">

        <div className="list-header">

          <h2>Employee List</h2>

          <div className="filters">

            <input
              className="search"
              type="text"
              placeholder="Search employee..."
              value={search}
              onChange={(e) =>
                setSearch(e.target.value)
              }
            />

            <select
              value={department}
              onChange={(e) =>
                setDepartment(e.target.value)
              }
            >
              <option value="">
                All Departments
              </option>

              {departments.map((dept) => (
                <option key={dept} value={dept}>
                  {dept}
                </option>
              ))}
            </select>

          </div>

        </div>

        {filteredEmployees.length === 0 ? (
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

              {filteredEmployees.map((employee) => (
                <tr key={employee.id}>

                  <td>{employee.id}</td>
                  <td>{employee.name}</td>
                  <td>{employee.email}</td>
                  <td>{employee.department}</td>
                  <td>₹{employee.salary}</td>

                  <td>

                    <button
                      className="edit-btn"
                      onClick={() =>
                        startEdit(employee)
                      }
                    >
                      Edit
                    </button>

                    <button
                      className="delete-btn"
                      onClick={() =>
                        deleteEmployee(employee.id)
                      }
                    >
                      Delete
                    </button>

                  </td>

                </tr>
              ))}

            </tbody>

          </table>
        )}

      </div>

    </div>
  );
}

export default App;