# Python Flask MVC Web App Tutorial — Student Management System
> **Tools:** Python 3.8+, VS Code, Flask, Bootstrap 5  
> **What you'll build:** A fully working Student Management web application using MVC architecture

---

## Table of Contents

1. [About This Project](#1-about-this-project)
2. [What is MVC in Web Apps?](#2-what-is-mvc-in-web-apps)
3. [Prerequisites & Setup](#3-prerequisites--setup)
4. [Project Structure](#4-project-structure)
5. [Phase 1 — The Model (Data Layer)](#5-phase-1--the-model-data-layer)
6. [Phase 2 — The View (Templates)](#6-phase-2--the-view-templates)
7. [Phase 3 — The Controller (Routes)](#7-phase-3--the-controller-routes)
8. [Phase 4 — Wire It Together & Run](#8-phase-4--wire-it-together--run)
9. [How MVC Works in This App](#9-how-mvc-works-in-this-app)
10. [Exercises for Students](#10-exercises-for-students)

---

## 1. About This Project

### The Problem

Imagine you are a university administrator. You have hundreds of students, and you need a system to:
- **Add** new students when they enroll
- **View** all student records at a glance
- **Edit** student information when details change (e.g., email, GPA)
- **Delete** students who have graduated or withdrawn
- **Track** how many students are enrolled and their academic performance

Currently, all of this is done with spreadsheets — messy, error-prone, and hard to share.

### The Solution

We will build a **Student Management System** — a web application that runs in the browser and provides a clean, professional interface to manage student records.

### What We Will Build

By the end of this 1-hour session, you will have a working web application with:

```
┌─────────────────────────────────────────────────────────────┐
│  🎓 Student Management System              Flask MVC Demo   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐           │
│  │  125   │  │   3.42 │  │   18   │  │   42   │           │
│  │ Total  │  │  Avg   │  │ Honor  │  │  New   │           │
│  │Students│  │  GPA   │  │  Roll  │  │ This Mo│           │
│  └────────┘  └────────┘  └────────┘  └────────┘           │
│                                                             │
│  ┌─ Add Student ──────┐  ┌─ Student Records ─────────────┐ │
│  │ Name:  [________]  │  │ ID │ Name    │ Email  │ GPA   │ │
│  │ Email: [________]  │  │ 1  │ Alice   │ ali@.. │ 3.80  │ │
│  │ Dept:  [▼ CS    ]  │  │ 2  │ Bob     │ bob@.. │ 3.50  │ │
│  │ GPA:   [________]  │  │ 3  │ Carol   │ car@.. │ 3.90  │ │
│  │ [  Add Student   ] │  │    │  ✏️  ✅  🗑️  │       │ │
│  └────────────────────┘  └───────────────────────────────┘ │
│                                                             │
│  📚 MVC Tutorial — Model · View · Controller               │
└─────────────────────────────────────────────────────────────┘
```

### Features We Will Implement

| Feature | Description |
|---------|-------------|
| **Dashboard** | Stats cards showing total students, average GPA, honor roll count |
| **Add Student** | Form with name, email, department, and GPA fields |
| **View All Students** | Table with color-coded GPA badges and department labels |
| **Edit Student** | Pre-filled form to update any student's information |
| **Delete Student** | Remove a student with confirmation dialog |
| **Honor Roll** | Automatically highlights students with GPA ≥ 3.5 |
| **Success/Error Messages** | Green/red notifications after every action |

### Learning Targets

By the end of this tutorial, you will understand:

| Target | What You'll Learn |
|--------|-------------------|
| **MVC Pattern** | How to separate data (Model), display (View), and logic (Controller) |
| **Flask Framework** | How to build web apps with Python's most popular micro-framework |
| **SQL Database** | How to create tables, insert, query, update, and delete records |
| **HTML Templates** | How Jinja2 templating works — loops, conditions, inheritance |
| **Bootstrap UI** | How to build professional-looking pages with minimal CSS |
| **CRUD Operations** | The fundamental pattern behind every web application |
| **HTTP Methods** | The difference between GET and POST requests |

### Why This Architecture?

Without MVC (everything in one file):
```
❌  app.py — 500+ lines of mixed SQL, HTML, routes, logic
❌  Hard to debug, hard to test, hard for teams to collaborate
```

With MVC (separated concerns):
```
✅  models.py    — Only data operations (~90 lines)
✅  routes.py    — Only request handling (~120 lines)
✅  templates/   — Only HTML display
✅  Easy to debug, test, and extend
```

---

## 2. What is MVC in Web Apps?

MVC (Model-View-Controller) separates a web application into three layers:

```
          Browser sends HTTP Request
                    │
                    ▼
    ┌───────────────────────────────┐
    │         CONTROLLER            │
    │     (routes.py — Flask)       │
    │                               │
    │  "A student clicked 'Add'.   │
    │   Let me validate the data,  │
    │   save it, and show results." │
    └───────┬───────────┬───────────┘
            │           │
            ▼           ▼
    ┌─────────────┐  ┌──────────────────┐
    │   MODEL     │  │      VIEW        │
    │ (models.py) │  │  (HTML Templates)│
    │             │  │                  │
    │ "I store    │  │ "I display       │
    │  students   │  │  students in     │
    │  in SQLite" │  │  a pretty table" │
    └─────────────┘  └──────────────────┘
```

| Component | Responsibility | Our Files |
|-----------|---------------|-----------|
| **Model** | Data storage, database queries, business rules | `models.py` |
| **View** | HTML pages, what users see in the browser | `templates/*.html` + `static/style.css` |
| **Controller** | Receives requests, coordinates Model ↔ View | `routes.py` |

### The Golden Rule of MVC

> **Each layer only talks to its neighbor. The Model and View never talk directly.**

```
Model  ◄──►  Controller  ◄──►  View
  ↕              ↕               ↕
Database     Python Logic     Browser
```

---

## 3. Prerequisites & Setup

### Step 1: Verify Python is Installed

Open a terminal (Command Prompt, PowerShell, or Terminal) and type:

```bash
python --version
```

You should see `Python 3.8.x` or higher. If `python` doesn't work, try `python3 --version`.

> **Don't have Python?** Download from [https://python.org/downloads](https://python.org/downloads)  
> ⚠️ On Windows, check **"Add Python to PATH"** during installation!

### Step 2: Install VS Code

Download from [https://code.visualstudio.com](https://code.visualstudio.com) and install.

Then install the **Python extension**:
1. Open VS Code
2. Press `Ctrl+Shift+X` (Extensions panel)
3. Search **"Python"** by Microsoft
4. Click **Install**

### Step 3: Create the Project Folder

```bash
mkdir StudentManagementMVC
cd StudentManagementMVC
```

### Step 4: Create a Virtual Environment

A virtual environment keeps our project's packages separate from the system Python.

```bash
# Create the virtual environment
python -m venv venv
```

**Activate it:**

| OS | Command |
|---|---|
| **Windows (CMD)** | `venv\Scripts\activate` |
| **Windows (PowerShell)** | `venv\Scripts\Activate.ps1` |
| **Mac / Linux** | `source venv/bin/activate` |

You should see `(venv)` appear at the start of your terminal prompt. This means you're inside the virtual environment.

### Step 5: Install Flask

```bash
pip install flask
```

That's it! Flask is our only dependency. No complex setup.

### Step 6: Open in VS Code

```bash
code .
```

VS Code will open with your project folder. You should see the `venv/` folder in the explorer.

---

## 4. Project Structure

Here is every file we will create:

```
StudentManagementMVC/
│
├── app.py                  ← Entry point (starts the server)
├── models.py               ← MODEL: Student data + SQLite database
├── routes.py               ← CONTROLLER: Flask routes (handles requests)
│
├── templates/              ← VIEW: HTML templates
│   ├── base.html           ← Shared layout (navbar, Bootstrap, footer)
│   ├── index.html          ← Home page (student list + add form + dashboard)
│   └── edit.html           ← Edit student page
│
├── static/
│   └── style.css           ← Custom CSS (small additions to Bootstrap)
│
├── requirements.txt        ← Python dependencies list
└── .gitignore              ← Files Git should ignore
```

**Total files to create: 9**  
**Build order: Model → Views → Controller → App** (we build bottom-up)

Let's start building!

---

## 5. Phase 1 — The Model (Data Layer)

The Model handles all data operations. It uses **SQLite** — a database that's built right into Python (no installation needed!).

### Create: `models.py`

Type or copy this into a new file called `models.py` in your project root:

```python
"""
MODEL — Data layer of the MVC pattern.

This file handles ALL data operations for students:
- Creates the database table
- Provides CRUD functions (Create, Read, Update, Delete)
- Computes statistics for the dashboard

IMPORTANT: This file has ZERO knowledge of:
- HTML templates (it doesn't know how students are displayed)
- Flask routes (it doesn't know what URL triggered the call)
- HTTP requests (it doesn't know about GET, POST, or browsers)

It ONLY knows about data.
"""

import sqlite3

DATABASE = "students.db"


def get_db():
    """
    Create a connection to the SQLite database.
    sqlite3.Row lets us access columns by name (e.g., row['name'])
    instead of by index (e.g., row[0]).
    """
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """
    Initialize the database:
    1. Create the 'students' table if it doesn't exist
    2. Insert sample data so the app isn't empty on first run

    This is called ONCE when the app starts.
    """
    conn = get_db()

    # Create table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            department TEXT DEFAULT 'Computer Science',
            gpa REAL DEFAULT 0.0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Insert sample data only if the table is empty
    count = conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]
    if count == 0:
        sample_students = [
            ("Alice Johnson",   "alice.johnson@university.ca",   "Computer Science",       3.85),
            ("Bob Smith",       "bob.smith@university.ca",       "Electrical Engineering",  3.42),
            ("Carol Williams",  "carol.williams@university.ca",  "Computer Science",       3.91),
            ("David Brown",     "david.brown@university.ca",     "Mathematics",            2.78),
            ("Emma Davis",      "emma.davis@university.ca",      "Computer Science",       3.65),
            ("Frank Miller",    "frank.miller@university.ca",    "Physics",                3.20),
            ("Grace Wilson",    "grace.wilson@university.ca",    "Electrical Engineering",  3.55),
            ("Henry Taylor",    "henry.taylor@university.ca",    "Mathematics",            2.95),
        ]
        conn.executemany(
            "INSERT INTO students (name, email, department, gpa) VALUES (?, ?, ?, ?)",
            sample_students,
        )

    conn.commit()
    conn.close()
    print("✅ Database initialized with student records!")


# ═══════════════════════════════════════════════════════
# CRUD OPERATIONS
# These are the ONLY functions the Controller should call.
# The Controller never writes SQL — it calls these instead.
# ═══════════════════════════════════════════════════════

def get_all_students():
    """READ — Retrieve all students, newest first."""
    conn = get_db()
    students = conn.execute(
        "SELECT * FROM students ORDER BY name ASC"
    ).fetchall()
    conn.close()
    return students


def get_student_by_id(student_id):
    """READ — Retrieve a single student by their ID."""
    conn = get_db()
    student = conn.execute(
        "SELECT * FROM students WHERE id = ?", (student_id,)
    ).fetchone()
    conn.close()
    return student


def add_student(name, email, department, gpa):
    """CREATE — Insert a new student into the database."""
    conn = get_db()
    conn.execute(
        "INSERT INTO students (name, email, department, gpa) VALUES (?, ?, ?, ?)",
        (name, email, department, gpa),
    )
    conn.commit()
    conn.close()


def update_student(student_id, name, email, department, gpa):
    """UPDATE — Modify an existing student's information."""
    conn = get_db()
    conn.execute(
        """UPDATE students
           SET name = ?, email = ?, department = ?, gpa = ?
           WHERE id = ?""",
        (name, email, department, gpa, student_id),
    )
    conn.commit()
    conn.close()


def delete_student(student_id):
    """DELETE — Remove a student from the database."""
    conn = get_db()
    conn.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    conn.close()


# ═══════════════════════════════════════════════════════
# STATISTICS — Used by the dashboard
# ═══════════════════════════════════════════════════════

def get_stats():
    """
    Compute summary statistics for the dashboard cards.
    Returns a dictionary with total, average GPA, honor roll count, etc.
    """
    conn = get_db()

    total = conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]
    honor_roll = conn.execute("SELECT COUNT(*) FROM students WHERE gpa >= 3.5").fetchone()[0]

    avg_row = conn.execute("SELECT AVG(gpa) FROM students").fetchone()[0]
    avg_gpa = round(avg_row, 2) if avg_row else 0.0

    # Count students per department
    departments = conn.execute(
        "SELECT department, COUNT(*) as count FROM students GROUP BY department ORDER BY count DESC"
    ).fetchall()

    conn.close()

    return {
        "total": total,
        "avg_gpa": avg_gpa,
        "honor_roll": honor_roll,
        "departments": departments,
    }
```

### What We Just Built

| Function | SQL Operation | Purpose |
|----------|-------------|---------|
| `init_db()` | `CREATE TABLE`, `INSERT` | Set up database + sample data |
| `get_all_students()` | `SELECT *` | List all students |
| `get_student_by_id(id)` | `SELECT WHERE id = ?` | Get one student |
| `add_student(...)` | `INSERT INTO` | Add new student |
| `update_student(...)` | `UPDATE WHERE id = ?` | Edit student |
| `delete_student(id)` | `DELETE WHERE id = ?` | Remove student |
| `get_stats()` | `COUNT`, `AVG`, `GROUP BY` | Dashboard numbers |

> **Note:** This file does not import Flask at all. The Model is pure Python + SQL.

---

## 6. Phase 2 — The View (Templates)

The View is what users see in the browser. We use **Jinja2** (Flask's template engine) to inject Python data into HTML, and **Bootstrap 5** for professional styling without writing much CSS.

### Create: `templates/base.html`

This is the **shared layout**. Every page inherits from it — like a parent class in OOP.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Student Manager{% endblock %} — MVC Demo</title>

    <!-- Bootstrap 5 CSS (loaded from CDN — no download needed) -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css"
          rel="stylesheet">

    <!-- Bootstrap Icons (for pencil, trash, check icons etc.) -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css"
          rel="stylesheet">

    <!-- Our custom CSS -->
    <link href="{{ url_for('static', filename='style.css') }}" rel="stylesheet">
</head>
<body>

    <!-- ═══════ NAVIGATION BAR ═══════ -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark shadow-sm">
        <div class="container">
            <a class="navbar-brand fw-bold" href="/">
                <i class="bi bi-mortarboard-fill me-2"></i>Student Manager
            </a>
            <span class="navbar-text text-light opacity-75">
                <small><i class="bi bi-code-slash me-1"></i>Built with Flask MVC</small>
            </span>
        </div>
    </nav>

    <!--
        ═══════ FLASH MESSAGES ═══════
        These are success/error notifications sent by the Controller.
        The Controller calls flash("message", "category") and
        the View displays them here automatically.
    -->
    <div class="container mt-3">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }} alert-dismissible fade show" role="alert">
                        {% if category == 'success' %}
                            <i class="bi bi-check-circle-fill me-2"></i>
                        {% elif category == 'danger' %}
                            <i class="bi bi-exclamation-triangle-fill me-2"></i>
                        {% else %}
                            <i class="bi bi-info-circle-fill me-2"></i>
                        {% endif %}
                        {{ message }}
                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}
    </div>

    <!--
        ═══════ MAIN CONTENT ═══════
        Child templates (index.html, edit.html) inject their content here.
        This is like an abstract method — each child implements it differently.
    -->
    <main class="container my-4">
        {% block content %}{% endblock %}
    </main>

    <!-- ═══════ FOOTER ═══════ -->
    <footer class="bg-light text-center text-muted py-3 mt-5 border-top">
        <small>
            <i class="bi bi-layers me-1"></i>
            MVC Architecture — <strong>Model</strong> (Python/SQLite) ·
            <strong>View</strong> (Jinja2/Bootstrap) ·
            <strong>Controller</strong> (Flask Routes)
        </small>
    </footer>

    <!-- Bootstrap 5 JavaScript (for dismissible alerts, tooltips, etc.) -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>

</body>
</html>
```

**Jinja2 Concepts Introduced:**
| Syntax | Meaning | Example |
|--------|---------|---------|
| `{% block name %}{% endblock %}` | Placeholder that child templates fill | `{% block content %}...{% endblock %}` |
| `{{ variable }}` | Print a variable's value | `{{ message }}` |
| `{% if condition %}` | Conditional logic | `{% if category == 'success' %}` |
| `{% for item in list %}` | Loop | `{% for message in messages %}` |
| `{{ url_for(...) }}` | Generate a URL safely | `{{ url_for('static', filename='style.css') }}` |

### Create: `templates/index.html`

The **home page** — displays the dashboard, add-student form, and student table.

```html
{% extends "base.html" %}
{% block title %}Home{% endblock %}

{% block content %}

<!-- ═══════════════════════════════════════
     SECTION 1: DASHBOARD STATS
     The Controller passes 'stats' dictionary to this template.
     We just display the numbers — no calculations here.
     ═══════════════════════════════════════ -->
<div class="row g-3 mb-4">
    <div class="col-6 col-md-3">
        <div class="card text-center border-0 shadow-sm stat-card">
            <div class="card-body">
                <i class="bi bi-people-fill stat-icon text-primary"></i>
                <div class="stat-number text-primary">{{ stats.total }}</div>
                <div class="stat-label">Total Students</div>
            </div>
        </div>
    </div>
    <div class="col-6 col-md-3">
        <div class="card text-center border-0 shadow-sm stat-card">
            <div class="card-body">
                <i class="bi bi-graph-up stat-icon text-success"></i>
                <div class="stat-number text-success">{{ stats.avg_gpa }}</div>
                <div class="stat-label">Average GPA</div>
            </div>
        </div>
    </div>
    <div class="col-6 col-md-3">
        <div class="card text-center border-0 shadow-sm stat-card">
            <div class="card-body">
                <i class="bi bi-trophy-fill stat-icon text-warning"></i>
                <div class="stat-number text-warning">{{ stats.honor_roll }}</div>
                <div class="stat-label">Honor Roll</div>
            </div>
        </div>
    </div>
    <div class="col-6 col-md-3">
        <div class="card text-center border-0 shadow-sm stat-card">
            <div class="card-body">
                <i class="bi bi-building stat-icon text-info"></i>
                <div class="stat-number text-info">{{ stats.departments|length }}</div>
                <div class="stat-label">Departments</div>
            </div>
        </div>
    </div>
</div>

<div class="row g-4">

    <!-- ═══════════════════════════════════════
         SECTION 2: ADD STUDENT FORM (Left Side)
         This form sends data to the Controller via POST.
         action="/add" → tells Flask which route handles this
         method="POST" → sends data in request body (not URL)
         ═══════════════════════════════════════ -->
    <div class="col-lg-4">
        <div class="card border-0 shadow-sm">
            <div class="card-header bg-dark text-white">
                <i class="bi bi-person-plus-fill me-2"></i>Add New Student
            </div>
            <div class="card-body">
                <form action="/add" method="POST">

                    <div class="mb-3">
                        <label for="name" class="form-label fw-semibold">
                            Full Name <span class="text-danger">*</span>
                        </label>
                        <input type="text" class="form-control" id="name"
                               name="name" placeholder="e.g., Jane Smith" required>
                    </div>

                    <div class="mb-3">
                        <label for="email" class="form-label fw-semibold">
                            Email <span class="text-danger">*</span>
                        </label>
                        <input type="email" class="form-control" id="email"
                               name="email" placeholder="e.g., jane@university.ca" required>
                    </div>

                    <div class="mb-3">
                        <label for="department" class="form-label fw-semibold">Department</label>
                        <select class="form-select" id="department" name="department">
                            <option value="Computer Science">Computer Science</option>
                            <option value="Electrical Engineering">Electrical Engineering</option>
                            <option value="Mathematics">Mathematics</option>
                            <option value="Physics">Physics</option>
                            <option value="Chemistry">Chemistry</option>
                            <option value="Biology">Biology</option>
                        </select>
                    </div>

                    <div class="mb-3">
                        <label for="gpa" class="form-label fw-semibold">
                            GPA <span class="text-danger">*</span>
                        </label>
                        <input type="number" class="form-control" id="gpa"
                               name="gpa" placeholder="e.g., 3.75"
                               min="0" max="4" step="0.01" required>
                    </div>

                    <button type="submit" class="btn btn-dark w-100">
                        <i class="bi bi-plus-lg me-2"></i>Add Student
                    </button>
                </form>
            </div>
        </div>
    </div>

    <!-- ═══════════════════════════════════════
         SECTION 3: STUDENT TABLE (Right Side)
         The Controller passes 'students' list to this template.
         We use a Jinja2 for-loop to render one row per student.
         ═══════════════════════════════════════ -->
    <div class="col-lg-8">
        <div class="card border-0 shadow-sm">
            <div class="card-header bg-dark text-white d-flex justify-content-between align-items-center">
                <span><i class="bi bi-table me-2"></i>Student Records</span>
                <span class="badge bg-light text-dark">{{ students|length }} students</span>
            </div>
            <div class="card-body p-0">

                {% if students|length == 0 %}
                    <!-- Empty state -->
                    <div class="text-center py-5 text-muted">
                        <i class="bi bi-inbox" style="font-size: 3rem;"></i>
                        <p class="mt-2">No students yet. Add one using the form!</p>
                    </div>
                {% else %}
                    <div class="table-responsive">
                        <table class="table table-hover mb-0 align-middle">
                            <thead class="table-light">
                                <tr>
                                    <th>ID</th>
                                    <th>Name</th>
                                    <th>Email</th>
                                    <th>Department</th>
                                    <th>GPA</th>
                                    <th class="text-center">Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                <!--
                                    JINJA2 FOR LOOP:
                                    'students' is a list of database rows passed by the Controller.
                                    Each 'student' is a dictionary-like row with keys: id, name, email, etc.
                                -->
                                {% for student in students %}
                                <tr>
                                    <td class="text-muted">{{ student.id }}</td>
                                    <td>
                                        <strong>{{ student.name }}</strong>
                                        {% if student.gpa >= 3.5 %}
                                            <span class="badge bg-warning text-dark ms-1" title="Honor Roll">⭐</span>
                                        {% endif %}
                                    </td>
                                    <td><small class="text-muted">{{ student.email }}</small></td>
                                    <td>
                                        <span class="badge
                                            {% if student.department == 'Computer Science' %}bg-primary
                                            {% elif student.department == 'Electrical Engineering' %}bg-info text-dark
                                            {% elif student.department == 'Mathematics' %}bg-success
                                            {% elif student.department == 'Physics' %}bg-secondary
                                            {% else %}bg-dark
                                            {% endif %}">
                                            {{ student.department }}
                                        </span>
                                    </td>
                                    <td>
                                        <!--
                                            GPA Color Coding:
                                            3.5+ = green (honor roll)
                                            3.0–3.49 = blue (good)
                                            2.0–2.99 = yellow (warning)
                                            below 2.0 = red (probation)
                                        -->
                                        {% if student.gpa >= 3.5 %}
                                            <span class="badge bg-success">{{ "%.2f"|format(student.gpa) }}</span>
                                        {% elif student.gpa >= 3.0 %}
                                            <span class="badge bg-primary">{{ "%.2f"|format(student.gpa) }}</span>
                                        {% elif student.gpa >= 2.0 %}
                                            <span class="badge bg-warning text-dark">{{ "%.2f"|format(student.gpa) }}</span>
                                        {% else %}
                                            <span class="badge bg-danger">{{ "%.2f"|format(student.gpa) }}</span>
                                        {% endif %}
                                    </td>
                                    <td class="text-center">
                                        <!--
                                            ACTION BUTTONS:
                                            Each button sends a request to a different Controller route.
                                            The View doesn't know what happens — it just links to the URL.
                                        -->
                                        <a href="/edit/{{ student.id }}"
                                           class="btn btn-sm btn-outline-primary me-1"
                                           title="Edit Student">
                                            <i class="bi bi-pencil"></i>
                                        </a>
                                        <a href="/delete/{{ student.id }}"
                                           class="btn btn-sm btn-outline-danger"
                                           title="Delete Student"
                                           onclick="return confirm('Are you sure you want to delete {{ student.name }}?')">
                                            <i class="bi bi-trash"></i>
                                        </a>
                                    </td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                {% endif %}

            </div>
        </div>
    </div>

</div>

{% endblock %}
```

### Create: `templates/edit.html`

The **edit page** — a form pre-filled with the student's current data.

```html
{% extends "base.html" %}
{% block title %}Edit Student{% endblock %}

{% block content %}

<div class="row justify-content-center">
    <div class="col-lg-6">

        <!-- Back button -->
        <a href="/" class="btn btn-outline-secondary mb-3">
            <i class="bi bi-arrow-left me-2"></i>Back to All Students
        </a>

        <div class="card border-0 shadow-sm">
            <div class="card-header bg-dark text-white">
                <i class="bi bi-pencil-square me-2"></i>Edit Student #{{ student.id }} — {{ student.name }}
            </div>
            <div class="card-body">
                <!--
                    The form fields are pre-filled with the current values.
                    value="{{ student.name }}" → shows existing data
                    action="/update/{{ student.id }}" → Controller knows which student to update
                -->
                <form action="/update/{{ student.id }}" method="POST">

                    <div class="mb-3">
                        <label for="name" class="form-label fw-semibold">
                            Full Name <span class="text-danger">*</span>
                        </label>
                        <input type="text" class="form-control" id="name"
                               name="name" value="{{ student.name }}" required>
                    </div>

                    <div class="mb-3">
                        <label for="email" class="form-label fw-semibold">
                            Email <span class="text-danger">*</span>
                        </label>
                        <input type="email" class="form-control" id="email"
                               name="email" value="{{ student.email }}" required>
                    </div>

                    <div class="mb-3">
                        <label for="department" class="form-label fw-semibold">Department</label>
                        <select class="form-select" id="department" name="department">
                            {% for dept in ['Computer Science', 'Electrical Engineering', 'Mathematics', 'Physics', 'Chemistry', 'Biology'] %}
                                <option value="{{ dept }}" {% if student.department == dept %}selected{% endif %}>
                                    {{ dept }}
                                </option>
                            {% endfor %}
                        </select>
                    </div>

                    <div class="mb-4">
                        <label for="gpa" class="form-label fw-semibold">
                            GPA <span class="text-danger">*</span>
                        </label>
                        <input type="number" class="form-control" id="gpa"
                               name="gpa" value="{{ student.gpa }}"
                               min="0" max="4" step="0.01" required>
                    </div>

                    <div class="d-flex gap-2">
                        <button type="submit" class="btn btn-primary flex-fill">
                            <i class="bi bi-save me-2"></i>Save Changes
                        </button>
                        <a href="/" class="btn btn-outline-secondary flex-fill">
                            <i class="bi bi-x-lg me-2"></i>Cancel
                        </a>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>

{% endblock %}
```

### Create: `static/style.css`

A small custom CSS file. Bootstrap does 95% of the work — we just add finishing touches.

```css
/*
 * VIEW LAYER — Custom Styles
 * Bootstrap handles most styling via classes in the HTML.
 * This file adds small visual enhancements.
 */

body {
    background-color: #f4f6f9;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
}

main {
    flex: 1;
}

/* ── Dashboard Stat Cards ── */
.stat-card {
    border-radius: 12px;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.stat-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1) !important;
}
.stat-icon {
    font-size: 1.5rem;
    display: block;
    margin-bottom: 4px;
}
.stat-number {
    font-size: 2rem;
    font-weight: 700;
    line-height: 1.2;
}
.stat-label {
    font-size: 0.8rem;
    color: #6c757d;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    font-weight: 600;
}

/* ── Card Styling ── */
.card {
    border-radius: 12px;
    overflow: hidden;
}
.card-header {
    border-bottom: none;
    padding: 14px 20px;
    font-weight: 600;
}

/* ── Table ── */
.table-hover tbody tr {
    transition: background-color 0.15s ease;
}

/* ── Form Focus States ── */
.form-control:focus,
.form-select:focus {
    border-color: #343a40;
    box-shadow: 0 0 0 0.2rem rgba(52, 58, 64, 0.15);
}

/* ── Buttons ── */
.btn {
    border-radius: 8px;
    font-weight: 500;
}

/* ── Navbar ── */
.navbar-brand {
    font-size: 1.3rem;
    letter-spacing: -0.3px;
}
```

---

## 7. Phase 3 — The Controller (Routes)

The Controller receives HTTP requests from the browser, calls the Model, and renders the View. It's the "traffic cop" of the application.

### Create: `routes.py`

```python
"""
CONTROLLER — Route handlers of the MVC pattern.

Each function here follows the same 3-step pattern:
    1. RECEIVE — Get the HTTP request from the browser
    2. PROCESS — Call the Model to get or modify data
    3. RESPOND — Render a View (template) or redirect

The Controller is the ONLY layer that knows about BOTH
the Model (models.py) and the View (templates/).

The Model doesn't know about Flask.
The View doesn't know about the database.
Only the Controller connects them.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash

# Import the Model — the Controller talks to the Model
import models

# Create a Blueprint (a way to organize routes in Flask)
main = Blueprint("main", __name__)


# ═══════════════════════════════════════════════
# ROUTE 1: HOME PAGE
# URL: GET /
# Purpose: Show all students + dashboard + add form
# MVC Flow: Controller → Model.get_all_students()
#                      → Model.get_stats()
#                      → View (index.html)
# ═══════════════════════════════════════════════
@main.route("/")
def index():
    """Display the home page."""

    # Ask the Model for data (Controller never writes SQL!)
    students = models.get_all_students()
    stats = models.get_stats()

    # Pass the data to the View and return the HTML
    return render_template("index.html", students=students, stats=stats)


# ═══════════════════════════════════════════════
# ROUTE 2: ADD A STUDENT
# URL: POST /add
# Purpose: Handle the "Add Student" form submission
# MVC Flow: View (form) → Controller (validate)
#         → Model.add_student() → Redirect to /
# ═══════════════════════════════════════════════
@main.route("/add", methods=["POST"])
def add_student():
    """Process the add student form."""

    # Step 1: Get data FROM the View (HTML form fields)
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    department = request.form.get("department", "Computer Science")
    gpa_text = request.form.get("gpa", "0")

    # Step 2: Validate (this is the Controller's job!)
    if not name or not email:
        flash("Name and email are required!", "danger")
        return redirect(url_for("main.index"))

    try:
        gpa = float(gpa_text)
        if gpa < 0 or gpa > 4:
            flash("GPA must be between 0.0 and 4.0", "danger")
            return redirect(url_for("main.index"))
    except ValueError:
        flash("GPA must be a valid number!", "danger")
        return redirect(url_for("main.index"))

    # Step 3: Tell the Model to save the data
    models.add_student(name, email, department, gpa)

    # Step 4: Send feedback and redirect back to home
    flash(f"Student '{name}' added successfully!", "success")
    return redirect(url_for("main.index"))


# ═══════════════════════════════════════════════
# ROUTE 3: SHOW EDIT FORM
# URL: GET /edit/<id>
# Purpose: Display the edit form pre-filled with student data
# MVC Flow: Controller → Model.get_student_by_id()
#         → View (edit.html)
# ═══════════════════════════════════════════════
@main.route("/edit/<int:student_id>")
def edit_student(student_id):
    """Show the edit form for a specific student."""

    # Ask the Model for this student's data
    student = models.get_student_by_id(student_id)

    if student is None:
        flash("Student not found!", "danger")
        return redirect(url_for("main.index"))

    # Pass the student data to the edit View
    return render_template("edit.html", student=student)


# ═══════════════════════════════════════════════
# ROUTE 4: PROCESS EDIT FORM
# URL: POST /update/<id>
# Purpose: Save the edited student data
# MVC Flow: View (form) → Controller (validate)
#         → Model.update_student() → Redirect to /
# ═══════════════════════════════════════════════
@main.route("/update/<int:student_id>", methods=["POST"])
def update_student(student_id):
    """Process the edit form submission."""

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    department = request.form.get("department", "Computer Science")
    gpa_text = request.form.get("gpa", "0")

    if not name or not email:
        flash("Name and email are required!", "danger")
        return redirect(url_for("main.edit_student", student_id=student_id))

    try:
        gpa = float(gpa_text)
        if gpa < 0 or gpa > 4:
            flash("GPA must be between 0.0 and 4.0", "danger")
            return redirect(url_for("main.edit_student", student_id=student_id))
    except ValueError:
        flash("GPA must be a valid number!", "danger")
        return redirect(url_for("main.edit_student", student_id=student_id))

    # Tell the Model to update
    models.update_student(student_id, name, email, department, gpa)

    flash(f"Student '{name}' updated successfully!", "success")
    return redirect(url_for("main.index"))


# ═══════════════════════════════════════════════
# ROUTE 5: DELETE A STUDENT
# URL: GET /delete/<id>
# Purpose: Remove a student from the database
# MVC Flow: Controller → Model.delete_student()
#         → Redirect to /
# ═══════════════════════════════════════════════
@main.route("/delete/<int:student_id>")
def delete_student(student_id):
    """Delete a student by ID."""

    student = models.get_student_by_id(student_id)

    if student is None:
        flash("Student not found!", "danger")
        return redirect(url_for("main.index"))

    models.delete_student(student_id)

    flash(f"Student '{student['name']}' has been removed.", "success")
    return redirect(url_for("main.index"))
```

### The Controller Pattern

Every single route in this file follows the exact same pattern:

```python
@main.route("/some-url")
def some_function():
    # 1. READ from View (if POST: request.form)
    # 2. VALIDATE (Controller's job)
    # 3. CALL Model (models.add_student, models.delete_student, etc.)
    # 4. RESPOND to View (render_template or redirect + flash)
```

---

## 8. Phase 4 — Wire It Together & Run

### Create: `app.py`

The entry point. Intentionally tiny — all the real work is in Model, View, and Controller.

```python
"""
APP — Entry point of the Student Management System.

This is where MVC comes together:
1. Create the Flask app
2. Initialize the Model (database)
3. Register the Controller (routes)
4. Start the web server

Notice how small this file is — that's the beauty of MVC!
Each layer handles its own responsibility.
"""

from flask import Flask
import models
from routes import main

# ── Create the Flask application ──
app = Flask(__name__)
app.secret_key = "student-mvc-tutorial-2025"  # Needed for flash messages

# ── Register the Controller ──
app.register_blueprint(main)

# ── Initialize the Model (create database + sample data) ──
models.init_db()

# ── Start the server ──
if __name__ == "__main__":
    print()
    print("=" * 55)
    print("   🎓 Student Management System — MVC Demo")
    print("   Open http://127.0.0.1:5000 in your browser")
    print("=" * 55)
    print()
    app.run(debug=True)
```

### Create: `requirements.txt`

```
flask
```

### Create: `.gitignore`

```
# Virtual environment
venv/
env/

# Database (auto-generated on first run)
students.db

# Python cache
__pycache__/
*.pyc
*.pyo

# VS Code
.vscode/

# OS files
.DS_Store
Thumbs.db
```

### Run the Application!

Make sure your virtual environment is activated (you should see `(venv)` in your terminal), then:

```bash
python app.py
```

You should see:

```
=======================================================
   🎓 Student Management System — MVC Demo
   Open http://127.0.0.1:5000 in your browser
=======================================================

✅ Database initialized with student records!
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

**Open your browser and go to:** [http://127.0.0.1:5000](http://127.0.0.1:5000)

### Test Everything

| # | Action | Steps | Expected Result |
|---|--------|-------|----------------|
| 1 | **View students** | Open the app | 8 sample students displayed in the table |
| 2 | **Check dashboard** | Look at the top | Total: 8, Avg GPA shown, Honor Roll count, 4 departments |
| 3 | **Add a student** | Fill form → click "Add Student" | Green success message, new student appears in table |
| 4 | **Add with empty name** | Leave name blank → submit | Red error message: "Name and email are required!" |
| 5 | **Add with invalid GPA** | Type "5.0" in GPA → submit | Red error: "GPA must be between 0.0 and 4.0" |
| 6 | **Edit a student** | Click ✏️ pencil on any row | Edit form appears with current data pre-filled |
| 7 | **Save edit** | Change the name → click "Save Changes" | Green success, redirected to home, name updated |
| 8 | **Delete a student** | Click 🗑️ trash → confirm | Green message, student removed, dashboard updates |
| 9 | **Honor Roll star** | Look at students with GPA ≥ 3.5 | They have a ⭐ badge next to their name |
| 10 | **GPA colors** | Look at the GPA column | Green ≥ 3.5, Blue ≥ 3.0, Yellow ≥ 2.0, Red < 2.0 |

---

## 9. How MVC Works in This App

### Complete Request Flow: "Add a Student"

```
BROWSER                     CONTROLLER              MODEL              VIEW
(User's screen)             (routes.py)           (models.py)      (templates/)
     │                          │                     │                  │
     │ 1. User fills form       │                     │                  │
     │    Name: "Zara Khan"     │                     │                  │
     │    Email: "zara@uni.ca"  │                     │                  │
     │    Dept: "CS"            │                     │                  │
     │    GPA: "3.75"           │                     │                  │
     │                          │                     │                  │
     │ 2. POST /add ───────────►│                     │                  │
     │    (form data)           │                     │                  │
     │                          │ 3. Validate:        │                  │
     │                          │    name? ✓          │                  │
     │                          │    email? ✓         │                  │
     │                          │    gpa valid? ✓     │                  │
     │                          │                     │                  │
     │                          │ 4. add_student(     │                  │
     │                          │    "Zara Khan",     │                  │
     │                          │    "zara@uni.ca",   │                  │
     │                          │    "CS", 3.75)      │                  │
     │                          │────────────────────►│                  │
     │                          │                     │ INSERT INTO      │
     │                          │                     │ students...      │
     │                          │      Done ◄─────────│                  │
     │                          │                     │                  │
     │ 5. Redirect to / ◄──────│                     │                  │
     │                          │                     │                  │
     │ 6. GET / ───────────────►│                     │                  │
     │                          │ 7. get_all_students()                  │
     │                          │────────────────────►│                  │
     │                          │     [8 students + Zara]                │
     │                          │◄────────────────────│                  │
     │                          │                     │                  │
     │                          │ 8. render_template( │                  │
     │                          │    "index.html",    │                  │
     │                          │     students=...,   │                  │
     │                          │     stats=...)──────────────────────►  │
     │                          │                     │   Generates HTML │
     │ 9. Full HTML page ◄─────────────────────────────────────────────│
     │                          │                     │                  │
     │ 10. Browser displays     │                     │                  │
     │     updated page with    │                     │                  │
     │     "Zara Khan" in table │                     │                  │
```

### The Separation Test

> **"If I change ONE layer, do the other layers need to change?"**

| What Changed | Model | View | Controller |
|---|---|---|---|
| Switch from SQLite to PostgreSQL | ✏️ Change queries | ✅ Untouched | ✅ Untouched |
| Redesign the UI with Tailwind CSS | ✅ Untouched | ✏️ Change templates | ✅ Untouched |
| Add a `/api/students` JSON endpoint | ✅ Untouched | ✅ Untouched | ✏️ Add one route |
| Add a "phone number" field | ✏️ Add column | ✏️ Add form field | ✏️ Handle new field |

The first three scenarios only require changing **one** layer. That's the power of MVC!

---

## 10. Exercises for Students

### Exercise 1: Add a Search Feature (15 min)
- Add a search form above the table in `index.html`
- Add a `search_students(query)` function in `models.py` using `WHERE name LIKE ?`
- Add a `GET /search` route in `routes.py`
- **Question:** Which layers did you change? Why?

### Exercise 2: Add a "Phone Number" Field (15 min)
- Add a `phone` column in the Model's CREATE TABLE
- Add a phone input field in both `index.html` and `edit.html`
- Handle it in the add/update routes in `routes.py`
- **Question:** Why did ALL three layers need to change?

### Exercise 3: Add a REST API Endpoint (10 min)
- Add this route to `routes.py`:
```python
from flask import jsonify

@main.route("/api/students")
def api_students():
    students = models.get_all_students()
    return jsonify([dict(s) for s in students])
```
- Visit `http://127.0.0.1:5000/api/students` in your browser
- **Question:** Which layers changed? (Answer: Only the Controller!)

### Exercise 4: Deploy to the Internet (Advanced)
- Sign up at [https://render.com](https://render.com) (free tier)
- Push your code to GitHub
- Create a new "Web Service" on Render pointing to your repo
- Your app is now live on the internet!

---

## Summary

| Concept | What We Learned |
|---------|----------------|
| **MVC Pattern** | Separate data (Model), display (View), and logic (Controller) |
| **Flask** | Python's lightweight web framework for building web apps |
| **SQLite** | A database built into Python — zero installation required |
| **Jinja2** | Template engine: `{{ variable }}`, `{% for %}`, `{% if %}`, `{% extends %}` |
| **Bootstrap 5** | Professional UI styling with CSS classes (no custom CSS needed) |
| **CRUD** | Create, Read, Update, Delete — the 4 fundamental database operations |
| **HTTP Methods** | GET (read data) vs POST (send data) |
| **Post/Redirect/Get** | Pattern that prevents "resubmit form?" browser warnings |

## Files Created

| # | File | MVC Layer | Lines | Purpose |
|---|------|-----------|-------|---------|
| 1 | `models.py` | Model | ~100 | Database + CRUD + statistics |
| 2 | `templates/base.html` | View | ~60 | Shared layout (navbar, alerts, footer) |
| 3 | `templates/index.html` | View | ~140 | Home page (dashboard + form + table) |
| 4 | `templates/edit.html` | View | ~70 | Edit student form |
| 5 | `static/style.css` | View | ~65 | Custom CSS enhancements |
| 6 | `routes.py` | Controller | ~120 | 5 Flask routes |
| 7 | `app.py` | Entry Point | ~20 | Wires MVC together |
| 8 | `requirements.txt` | Config | 1 | Dependencies |
| 9 | `.gitignore` | Config | ~15 | Git ignore rules |


---

