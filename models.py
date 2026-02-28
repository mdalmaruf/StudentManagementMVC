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
    """READ — Retrieve all students, ordered by name."""
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
