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
