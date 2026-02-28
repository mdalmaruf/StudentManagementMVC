# MVC Debugging Guide — Understanding Request/Response Flow

> **For:** Java Swing (Desktop) + Python Flask (Web) Student Management Projects  
> **Goal:** Learn how to trace, debug, and understand every step of the MVC cycle

---

## Table of Contents

1. [How MVC Flow Works — The Big Picture](#1-how-mvc-flow-works--the-big-picture)
2. [Java Swing MVC — How Events Flow](#2-java-swing-mvc--how-events-flow)
3. [Flask Web MVC — How HTTP Requests Flow](#3-flask-web-mvc--how-http-requests-flow)
4. [Debugging Java Swing in VS Code](#4-debugging-java-swing-in-vs-code)
5. [Debugging Flask in VS Code](#5-debugging-flask-in-vs-code)
6. [Adding Print/Log Statements for Tracing](#6-adding-printlog-statements-for-tracing)
7. [Common Bugs and How to Find Them](#7-common-bugs-and-how-to-find-them)

---

## 1. How MVC Flow Works — The Big Picture

### Desktop App (Java Swing) vs Web App (Flask)

The MVC pattern is the same concept, but the **trigger mechanism** is different:

```
JAVA SWING (Desktop)                    FLASK (Web)
══════════════════════                  ══════════════════════

User clicks a button                   User clicks a link or submits a form
       │                                       │
       ▼                                       ▼
ActionListener fires                    HTTP Request sent (GET or POST)
       │                                       │
       ▼                                       ▼
Controller method runs                  Route function runs
       │                                       │
       ▼                                       ▼
Controller calls Model                  Controller calls Model
       │                                       │
       ▼                                       ▼
Model reads/writes data                 Model reads/writes database
       │                                       │
       ▼                                       ▼
Controller updates View                 Controller renders template
       │                                       │
       ▼                                       ▼
View repaints the screen               Browser displays HTML response
```

The key difference:
- **Java Swing:** Everything happens in ONE running program. The View, Controller, 
  and Model are all objects in memory talking to each other directly.
- **Flask:** The browser and server are SEPARATE. The browser sends an HTTP request, 
  the server processes it, and sends back HTML. Then the connection closes.

---

## 2. Java Swing MVC — How Events Flow

### Example: User Clicks "Add Student"

Let's trace EXACTLY what happens, line by line:

```
STEP 1: USER ACTION
═══════════════════
User types "Zara Khan" in name field, "zara@uni.ca" in email, "3.75" in GPA
User clicks the "Add Student" button

STEP 2: VIEW → CONTROLLER (Event fires)
════════════════════════════════════════
The button click triggers an ActionListener.
WHERE does this connection happen? In the Controller's constructor:

    File: StudentController.java, line ~30
    ┌─────────────────────────────────────────────────────────────┐
    │ this.view.addAddListener(e -> addStudent());                │
    │                          ▲              ▲                   │
    │                          │              │                   │
    │            "when button is clicked"   "call this method"    │
    └─────────────────────────────────────────────────────────────┘

    This line says: "View, when your Add button is clicked, call MY addStudent() method."

STEP 3: CONTROLLER READS FROM VIEW
═══════════════════════════════════
    File: StudentController.java → addStudent() method

    String name = view.getNameInput();      // Returns "Zara Khan"
    String email = view.getEmailInput();    // Returns "zara@uni.ca"
    String gpaText = view.getGpaInput();    // Returns "3.75"

    HOW does this work? The View has public getter methods:

    File: StudentView.java
    ┌──────────────────────────────────────────────────────┐
    │ public String getNameInput() {                       │
    │     return nameField.getText().trim();  // reads the │
    │ }                                       // text field│
    └──────────────────────────────────────────────────────┘

STEP 4: CONTROLLER VALIDATES
════════════════════════════
    if (name.isEmpty() || email.isEmpty() || gpaText.isEmpty()) {
        view.showError("Please fill in all fields.");  // show error popup
        return;  // STOP HERE — don't touch the Model
    }

    double gpa = Double.parseDouble(gpaText);  // Convert "3.75" → 3.75
    if (gpa < 0.0 || gpa > 4.0) {
        view.showError("GPA must be between 0.0 and 4.0");
        return;  // STOP HERE
    }

STEP 5: CONTROLLER → MODEL (Save data)
═══════════════════════════════════════
    Student added = model.addStudent(name, email, gpa);
                    ▲
                    │
    File: StudentModel.java → addStudent()
    ┌──────────────────────────────────────────────────────┐
    │ public Student addStudent(String name, ...) {        │
    │     Student student = new Student(nextId++, ...);    │
    │     students.add(student);  // adds to ArrayList     │
    │     return student;                                  │
    │ }                                                    │
    └──────────────────────────────────────────────────────┘

STEP 6: CONTROLLER → VIEW (Refresh display)
════════════════════════════════════════════
    refreshTable();        // reload all students into the table
    view.clearInputFields(); // clear the form
    view.setStatus("Added: Zara Khan (ID: 4)");

    Inside refreshTable():
    ┌──────────────────────────────────────────────────────┐
    │ List<Student> allStudents = model.getAllStudents();   │
    │ view.displayStudents(allStudents);                   │
    │     ▲                    ▲                           │
    │     │                    │                           │
    │  Model returns data   View redraws the JTable        │
    └──────────────────────────────────────────────────────┘

STEP 7: VIEW REPAINTS
═════════════════════
    The JTable now shows the new student. The status bar updates.
    The user sees the result.
```

### The Complete Chain (Summary)

```
Button Click → ActionListener → Controller.addStudent()
    → view.getNameInput()           [read from View]
    → validate(name, email, gpa)    [Controller logic]
    → model.addStudent(...)         [write to Model]
    → model.getAllStudents()         [read from Model]
    → view.displayStudents(...)     [update View]
```

---

## 3. Flask Web MVC — How HTTP Requests Flow

### Example: User Clicks "Add Student"

```
STEP 1: USER ACTION (in Browser)
═════════════════════════════════
User fills in the form on index.html:
    Name: "Zara Khan"
    Email: "zara@uni.ca"
    Department: "Computer Science"
    GPA: "3.75"
User clicks the "Add Student" button.

STEP 2: BROWSER → SERVER (HTTP Request)
════════════════════════════════════════
The browser sends an HTTP POST request. You can SEE this in the browser DevTools:

    POST /add HTTP/1.1
    Content-Type: application/x-www-form-urlencoded

    name=Zara+Khan&email=zara%40uni.ca&department=Computer+Science&gpa=3.75

    HOW does this happen? Because of the HTML form tag:

    File: templates/index.html
    ┌──────────────────────────────────────────────────┐
    │ <form action="/add" method="POST">               │
    │        ▲              ▲                           │
    │        │              │                           │
    │   "send to this URL" "use POST method"           │
    │                                                  │
    │   <input name="name" ...>   ← becomes name=...  │
    │   <input name="email" ...>  ← becomes email=... │
    │   <input name="gpa" ...>    ← becomes gpa=...   │
    │ </form>                                          │
    └──────────────────────────────────────────────────┘

STEP 3: FLASK FINDS THE RIGHT ROUTE (Controller)
═════════════════════════════════════════════════
Flask looks at the request: "POST /add" and finds:

    File: routes.py
    ┌──────────────────────────────────────────────────┐
    │ @main.route("/add", methods=["POST"])             │
    │ def add_student():          ← THIS function runs │
    └──────────────────────────────────────────────────┘

    Flask matches "/add" + "POST" → calls add_student()

STEP 4: CONTROLLER READS FROM REQUEST
══════════════════════════════════════
    name = request.form.get("name", "").strip()       # "Zara Khan"
    email = request.form.get("email", "").strip()     # "zara@uni.ca"
    department = request.form.get("department", ...)   # "Computer Science"
    gpa_text = request.form.get("gpa", "0")           # "3.75"

    WHERE does request.form come from?
    Flask automatically parses the POST body and puts
    form fields into request.form (a dictionary).

    This is the equivalent of view.getNameInput() in Java Swing.

STEP 5: CONTROLLER VALIDATES
═════════════════════════════
    if not name or not email:
        flash("Name and email are required!", "danger")
        return redirect(url_for("main.index"))  # go back to home

    gpa = float(gpa_text)    # Convert "3.75" → 3.75
    if gpa < 0 or gpa > 4:
        flash("GPA must be between 0.0 and 4.0", "danger")
        return redirect(url_for("main.index"))

STEP 6: CONTROLLER → MODEL (Save data)
═══════════════════════════════════════
    models.add_student(name, email, department, gpa)
           ▲
           │
    File: models.py → add_student()
    ┌──────────────────────────────────────────────────┐
    │ def add_student(name, email, department, gpa):   │
    │     conn = get_db()                              │
    │     conn.execute(                                │
    │         "INSERT INTO students ... VALUES (?,?)", │
    │         (name, email, department, gpa)            │
    │     )                                            │
    │     conn.commit()                                │
    │     conn.close()                                 │
    └──────────────────────────────────────────────────┘

STEP 7: CONTROLLER → REDIRECT
══════════════════════════════
    flash(f"Student '{name}' added successfully!", "success")
    return redirect(url_for("main.index"))

    This sends an HTTP response back to the browser:

        HTTP/1.1 302 Found
        Location: /

    The browser sees "302 redirect" and automatically makes a NEW request:

        GET / HTTP/1.1

STEP 8: SECOND REQUEST — HOME PAGE LOADS
═════════════════════════════════════════
    Flask receives GET / and calls index():

    @main.route("/")
    def index():
        students = models.get_all_students()  ← now includes Zara Khan!
        stats = models.get_stats()
        return render_template("index.html", students=students, stats=stats)

    render_template does:
    1. Opens templates/index.html
    2. Runs the Jinja2 code ({% for student in students %} etc.)
    3. Produces a complete HTML string
    4. Sends it back to the browser

STEP 9: BROWSER RENDERS
════════════════════════
    Browser receives the HTML, renders it, and the user sees:
    - Green success alert: "Student 'Zara Khan' added successfully!"
    - Zara Khan appears in the table
    - Dashboard stats updated
```

### Why Two Requests? (Post/Redirect/Get Pattern)

```
Request 1: POST /add         → saves data → responds with "redirect to /"
Request 2: GET /              → reads data → responds with HTML page

Why not just render the page directly after POST?
Because if the user refreshes the browser after a POST, the browser will ask:
"Do you want to resubmit the form?" — which would add the student AGAIN.

The redirect prevents this. After the redirect, refreshing just reloads GET /.
```

---

## 4. Debugging Java Swing in VS Code

### Step 1: Install Required Extensions

Make sure you have the **Extension Pack for Java** installed (it includes the debugger).

### Step 2: Add Breakpoints

A **breakpoint** is a line where the program will PAUSE so you can inspect variables.

Click on the **left margin** (the gutter) next to a line number. A red dot appears.

**Best places to add breakpoints in our Student MVC app:**

```java
// In StudentController.java:

private void addStudent() {
    String name = view.getNameInput();      // ← BREAKPOINT HERE (Step 3)
    String email = view.getEmailInput();
    String gpaText = view.getGpaInput();
    
    // ... validation ...
    
    Student added = model.addStudent(name, email, gpa);  // ← BREAKPOINT HERE (Step 5)
    
    refreshTable();  // ← BREAKPOINT HERE (Step 6)
}
```

```java
// In StudentModel.java:

public Student addStudent(String name, String email, double gpa) {
    Student student = new Student(nextId++, name, email, gpa);  // ← BREAKPOINT HERE
    students.add(student);
    return student;
}
```

### Step 3: Start Debugging

1. Open `App.java`
2. Press `F5` (or click **Run → Start Debugging**)
3. Or click the **"Debug"** button above the `main` method

### Step 4: Using the Debugger

When the program hits a breakpoint, it PAUSES. You'll see:

```
┌─────────────────────────────────────────────────────────────┐
│ VS Code Debug Controls (top of screen):                     │
│                                                             │
│   ▶ Continue (F5)     — Resume until next breakpoint        │
│   ⤵ Step Over (F10)   — Execute this line, go to next       │
│   ⤓ Step Into (F11)   — Go INSIDE the method being called   │
│   ⤒ Step Out (Shift+F11) — Finish this method, go back      │
│   ⟳ Restart            — Restart the app                    │
│   ■ Stop               — Kill the app                       │
│                                                             │
│ Left Panel (VARIABLES):                                     │
│   name = "Zara Khan"                                        │
│   email = "zara@uni.ca"                                     │
│   gpaText = "3.75"                                          │
│   gpa = 3.75                                                │
│   this.model.students = [Student@1, Student@2, ...]         │
│                                                             │
│ Left Panel (CALL STACK):                                    │
│   addStudent()           ← you are here                     │
│   lambda$0()             ← the ActionListener               │
│   ActionEvent.dispatch() ← Swing event system               │
└─────────────────────────────────────────────────────────────┘
```

### Step 5: Tracing the MVC Flow with the Debugger

Here's the exact debugging workflow:

```
1. Set breakpoint in Controller: addStudent(), first line
2. Run the app (F5)
3. Click "Add Student" in the GUI
4. Program PAUSES at your breakpoint
5. Look at VARIABLES panel:
   - name = "Zara Khan"    ← data FROM the View
   - email = "zara@uni.ca"
6. Press F10 (Step Over) to move line by line
7. When you reach: model.addStudent(...)
   Press F11 (Step Into) ← this JUMPS INTO the Model!
8. Now you're INSIDE StudentModel.addStudent()
   - You can see the students ArrayList
   - Watch the new Student being created
9. Press Shift+F11 (Step Out) to go back to the Controller
10. Continue stepping to see refreshTable() update the View
```

### Debug Configuration File (if VS Code doesn't auto-detect)

Create `.vscode/launch.json`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "type": "java",
            "name": "Run Student MVC",
            "request": "launch",
            "mainClass": "App",
            "classPaths": ["out"],
            "preLaunchTask": "javac"
        }
    ]
}
```

---

## 5. Debugging Flask in VS Code

### Step 1: Install the Python Extension

Make sure the **Python** extension by Microsoft is installed.

### Step 2: Create Debug Configuration

Create a file `.vscode/launch.json` in your project:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Flask: Student Manager",
            "type": "debugpy",
            "request": "launch",
            "module": "flask",
            "args": ["run", "--debug"],
            "env": {
                "FLASK_APP": "app.py"
            },
            "jinja": true
        }
    ]
}
```

The `"jinja": true` line enables debugging inside HTML templates too!

### Step 3: Add Breakpoints

Click the left margin to add red breakpoint dots:

```python
# In routes.py — add_student():

@main.route("/add", methods=["POST"])
def add_student():
    name = request.form.get("name", "").strip()      # ← BREAKPOINT HERE
    email = request.form.get("email", "").strip()
    department = request.form.get("department", ...)
    gpa_text = request.form.get("gpa", "0")

    # ... validation ...

    models.add_student(name, email, department, gpa)  # ← BREAKPOINT HERE
    
    flash(f"Student '{name}' added!", "success")       # ← BREAKPOINT HERE
    return redirect(url_for("main.index"))
```

```python
# In models.py — add_student():

def add_student(name, email, department, gpa):
    conn = get_db()                                    # ← BREAKPOINT HERE
    conn.execute(
        "INSERT INTO students ... VALUES (?, ?, ?, ?)",
        (name, email, department, gpa),                # ← BREAKPOINT HERE
    )
    conn.commit()
    conn.close()
```

### Step 4: Start Debugging

1. Press `F5` (or Run → Start Debugging)
2. Select "Flask: Student Manager" from the dropdown
3. Flask starts in debug mode
4. Open `http://127.0.0.1:5000` in your browser
5. Fill in the form and click "Add Student"
6. VS Code will PAUSE at your breakpoint!

### Step 5: Using the Flask Debugger

```
┌─────────────────────────────────────────────────────────────┐
│ VS Code Debug Controls:                                     │
│                                                             │
│   ▶ Continue (F5)      — Resume until next breakpoint       │
│   ⤵ Step Over (F10)    — Execute this line, go to next      │
│   ⤓ Step Into (F11)    — Go INTO the function being called  │
│   ⤒ Step Out (Shift+F11) — Finish this function, return     │
│                                                             │
│ Left Panel (VARIABLES):                                     │
│   name = "Zara Khan"                                        │
│   email = "zara@uni.ca"                                     │
│   department = "Computer Science"                           │
│   gpa_text = "3.75"                                         │
│   gpa = 3.75                                                │
│                                                             │
│   request.form = ImmutableMultiDict([                       │
│       ('name', 'Zara Khan'),                                │
│       ('email', 'zara@uni.ca'),                             │
│       ('department', 'Computer Science'),                   │
│       ('gpa', '3.75')                                       │
│   ])                                                        │
│                                                             │
│ Left Panel (CALL STACK):                                    │
│   add_student()          ← you are here (routes.py)         │
│   Flask.dispatch_request()                                  │
│   Flask.full_dispatch_request()                             │
│   Flask.wsgi_app()                                          │
└─────────────────────────────────────────────────────────────┘
```

### Step 6: Tracing the Full MVC Cycle

```
1. Set breakpoint at: name = request.form.get("name")
2. Start debugging (F5)
3. Open browser → fill form → click Add Student
4. VS Code PAUSES. Now trace:
   
   F10 → name = "Zara Khan"           (read from View/form)
   F10 → email = "zara@uni.ca"        (read from View/form)
   F10 → gpa_text = "3.75"            (read from View/form)
   F10 → validation passes...
   
   F11 → STEP INTO models.add_student()   ← you jump to models.py!
         Now you're in the MODEL layer.
         F10 → conn = get_db()             (database connects)
         F10 → conn.execute(INSERT...)     (data saved!)
         F10 → conn.commit()               (confirmed)
         Shift+F11 → back to routes.py     ← back to CONTROLLER
   
   F10 → flash("Student added!")       (message for View)
   F10 → return redirect(...)          (send browser to /)
   
   F5  → Continue... Flask handles GET / request
         index() runs, calls models.get_all_students()
         returns render_template("index.html", ...)
         Browser shows updated page!
```

### Using Browser Developer Tools (F12)

This is ESSENTIAL for debugging the web MVC flow:

```
1. Open your browser (Chrome/Firefox/Edge)
2. Press F12 to open Developer Tools
3. Click the "Network" tab
4. Now click "Add Student" in your app

You will see TWO requests:

┌────────┬────────┬────────┬──────────────────────────────┐
│ Method │ URL    │ Status │ What happened                │
├────────┼────────┼────────┼──────────────────────────────┤
│ POST   │ /add   │ 302    │ Controller saved data,       │
│        │        │        │ responded with "redirect"    │
├────────┼────────┼────────┼──────────────────────────────┤
│ GET    │ /      │ 200    │ Home page loaded with        │
│        │        │        │ updated student list         │
└────────┴────────┴────────┴──────────────────────────────┘

Click on the POST /add request to see:
- "Headers" tab → shows the request URL, method, status
- "Payload" tab → shows the form data sent (name, email, gpa)
- "Response" tab → shows the redirect response

Click on the GET / request to see:
- "Response" tab → shows the full HTML returned by the server
```

---

## 6. Adding Print/Log Statements for Tracing

If you want to see the MVC flow without the debugger, add print statements.

### Java Swing — Add to StudentController.java

```java
private void addStudent() {
    System.out.println("═══ MVC FLOW: Add Student ═══");
    
    // Step: Read from View
    String name = view.getNameInput();
    String email = view.getEmailInput();
    String gpaText = view.getGpaInput();
    System.out.println("[CONTROLLER] Read from VIEW: name=" + name 
                       + ", email=" + email + ", gpa=" + gpaText);
    
    // Step: Validate
    if (name.isEmpty() || email.isEmpty() || gpaText.isEmpty()) {
        System.out.println("[CONTROLLER] Validation FAILED: empty fields");
        view.showError("Please fill in all fields.");
        return;
    }
    
    double gpa = Double.parseDouble(gpaText);
    System.out.println("[CONTROLLER] Validation PASSED");
    
    // Step: Call Model
    System.out.println("[CONTROLLER] Calling MODEL.addStudent()...");
    Student added = model.addStudent(name, email, gpa);
    System.out.println("[MODEL] Student saved: " + added);
    
    // Step: Update View
    System.out.println("[CONTROLLER] Refreshing VIEW...");
    refreshTable();
    view.clearInputFields();
    view.setStatus("Added: " + added.getName());
    System.out.println("[VIEW] Table refreshed, form cleared");
    System.out.println("═══ MVC FLOW COMPLETE ═══\n");
}
```

**Terminal output when you click "Add Student":**
```
═══ MVC FLOW: Add Student ═══
[CONTROLLER] Read from VIEW: name=Zara Khan, email=zara@uni.ca, gpa=3.75
[CONTROLLER] Validation PASSED
[CONTROLLER] Calling MODEL.addStudent()...
[MODEL] Student saved: Student{id=4, name='Zara Khan', email='zara@uni.ca', gpa=3.75}
[CONTROLLER] Refreshing VIEW...
[VIEW] Table refreshed, form cleared
═══ MVC FLOW COMPLETE ═══
```

### Flask — Add to routes.py

```python
@main.route("/add", methods=["POST"])
def add_student():
    print("\n═══ MVC FLOW: Add Student ═══")
    
    # Step: Read from View (HTTP form)
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    department = request.form.get("department", "Computer Science")
    gpa_text = request.form.get("gpa", "0")
    print(f"[CONTROLLER] Read from VIEW: name={name}, email={email}, "
          f"dept={department}, gpa={gpa_text}")
    print(f"[CONTROLLER] Request method: {request.method}, URL: {request.url}")
    
    # Step: Validate
    if not name or not email:
        print("[CONTROLLER] Validation FAILED: missing fields")
        flash("Name and email are required!", "danger")
        return redirect(url_for("main.index"))
    
    gpa = float(gpa_text)
    print(f"[CONTROLLER] Validation PASSED, gpa={gpa}")
    
    # Step: Call Model
    print(f"[CONTROLLER] Calling MODEL.add_student()...")
    models.add_student(name, email, department, gpa)
    print(f"[MODEL] Student saved to database")
    
    # Step: Redirect (triggers View refresh)
    print(f"[CONTROLLER] Sending redirect to /")
    print("═══ MVC FLOW COMPLETE ═══\n")
    
    flash(f"Student '{name}' added successfully!", "success")
    return redirect(url_for("main.index"))
```

**Terminal output when you click "Add Student":**
```
═══ MVC FLOW: Add Student ═══
[CONTROLLER] Read from VIEW: name=Zara Khan, email=zara@uni.ca, dept=Computer Science, gpa=3.75
[CONTROLLER] Request method: POST, URL: http://127.0.0.1:5000/add
[CONTROLLER] Validation PASSED, gpa=3.75
[CONTROLLER] Calling MODEL.add_student()...
[MODEL] Student saved to database
[CONTROLLER] Sending redirect to /
═══ MVC FLOW COMPLETE ═══

127.0.0.1 - - "POST /add HTTP/1.1" 302 -     ← Flask's built-in log
127.0.0.1 - - "GET / HTTP/1.1" 200 -          ← the redirect!
```

### Flask — Add to models.py

```python
def add_student(name, email, department, gpa):
    """CREATE — Insert a new student into the database."""
    print(f"  [MODEL] add_student() called with: {name}, {email}, {department}, {gpa}")
    conn = get_db()
    conn.execute(
        "INSERT INTO students (name, email, department, gpa) VALUES (?, ?, ?, ?)",
        (name, email, department, gpa),
    )
    conn.commit()
    conn.close()
    print(f"  [MODEL] INSERT committed to SQLite database")
```

---

## 7. Common Bugs and How to Find Them

### Java Swing Common Bugs

| Bug | Symptom | How to Debug |
|-----|---------|-------------|
| Button does nothing | Click has no effect | Check if `addAddListener()` is called in Controller constructor. Set breakpoint in the listener. |
| Table doesn't update | New student not shown | Set breakpoint in `refreshTable()`. Check if `model.getAllStudents()` returns the new student. |
| Wrong data displayed | Table shows stale data | Check if `displayStudents()` clears old rows first (`tableModel.setRowCount(0)`). |
| NullPointerException | App crashes | Check VARIABLES panel. One of your objects is null. Trace back to where it should have been created. |
| NumberFormatException | Error on "Add" | User typed non-numeric GPA. Check if your try/catch handles this. |

**Debug approach:**
```
1. Set breakpoint at the START of the Controller method
2. Step Over (F10) line by line
3. After each line, check the VARIABLES panel
4. When a variable has an unexpected value → you found the bug
```

### Flask Common Bugs

| Bug | Symptom | How to Debug |
|-----|---------|-------------|
| 404 Not Found | Page doesn't exist | Check if route URL matches the link. Check Blueprint registered in app.py. |
| 405 Method Not Allowed | Form submit fails | Check `methods=["POST"]` in the route decorator. |
| Template not found | Jinja2 error | Check file is in `templates/` folder. Check filename spelling. |
| Form data is None | `request.form` empty | Check `name="..."` attribute on form inputs matches what you read in routes.py. |
| Flash message not showing | No green/red alert | Check `app.secret_key` is set. Check `get_flashed_messages()` in base.html. |
| Changes not reflected | Old data showing | Check if you called `conn.commit()` after INSERT/UPDATE. |
| CSS not loading | No styling | Check `url_for('static', filename='style.css')` and file is in `static/`. |

**Debug approach for Flask:**
```
1. Check the TERMINAL — Flask prints errors with tracebacks
2. Check BROWSER DevTools (F12) → Network tab → look for red requests
3. Check BROWSER DevTools → Console tab → look for JavaScript errors
4. Add print() statements in routes.py to trace the flow
5. Use VS Code debugger with breakpoints for complex issues
```

### The Most Important Debugging Question

When something doesn't work, ask yourself:

```
"WHERE in the MVC flow did things go wrong?"

1. Is the VIEW sending the right data?
   → Check browser DevTools → Network → Payload
   → Or add print(request.form) in the Controller

2. Is the CONTROLLER receiving and processing correctly?
   → Add breakpoint at the start of the route function
   → Check all variables in the VARIABLES panel

3. Is the MODEL saving/reading correctly?
   → Add breakpoint inside the model function
   → For Flask: open students.db with a SQLite viewer
   → Or add print() in the model functions

4. Is the VIEW displaying the result correctly?
   → Check what data the Controller passes to the template
   → Add print(students) before render_template()
   → Check the HTML source in browser (right-click → View Page Source)
```

---

## Quick Reference: Debug Shortcuts

| Action | Windows/Linux | Mac |
|--------|--------------|-----|
| **Start Debugging** | `F5` | `F5` |
| **Stop Debugging** | `Shift+F5` | `Shift+F5` |
| **Step Over** (next line) | `F10` | `F10` |
| **Step Into** (go inside function) | `F11` | `F11` |
| **Step Out** (finish function) | `Shift+F11` | `Shift+F11` |
| **Continue** (run to next breakpoint) | `F5` | `F5` |
| **Toggle Breakpoint** | `F9` | `F9` |
| **Debug Console** (type expressions) | `Ctrl+Shift+Y` | `Cmd+Shift+Y` |
| **Browser DevTools** | `F12` | `Cmd+Opt+I` |

---

*This guide covers debugging for both the Java Swing and Flask MVC Student Management tutorials.*
