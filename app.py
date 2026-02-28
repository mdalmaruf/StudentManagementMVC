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
