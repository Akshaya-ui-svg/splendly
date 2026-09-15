from flask import Flask, render_template, request, redirect, url_for, flash
from database.db import init_db, seed_db, create_user
from werkzeug.security import generate_password_hash
import re

app = Flask(__name__)
app.secret_key = 'dev-secret-key-for-spendly'

with app.app_context():
    init_db()
    seed_db()



# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        # Basic validation
        if not name or not email or not password:
            flash("All fields are required", "error")
            return render_template("register.html")

        # Email validation
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash("Please enter a valid email address", "error")
            return render_template("register.html")

        # Password strength validation
        if len(password) < 8:
            flash("Password must be at least 8 characters long", "error")
            return render_template("register.html")

        try:
            hashed_pw = generate_password_hash(password)
            create_user(name, email, hashed_pw)
            flash("Account created successfully! Please sign in.", "success")
            return redirect(url_for("login"))
        except Exception:
            # Assuming IntegrityError for duplicate email is the primary case
            flash("This email is already registered", "error")
            return render_template("register.html")

    return render_template("register.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout")
def logout():
    return "Logout — coming in Step 3"


@app.route("/profile")
def profile():
    return "Profile page — coming in Step 4"


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    app.run(debug=True, port=5001)
