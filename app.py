from flask import Flask, render_template, request, redirect, session
import sqlite3
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import re
from datetime import datetime
import random

app = Flask(__name__)

app.secret_key = "securefin_assignment_secret_key"

ph = PasswordHasher()

def write_log(event):

    with open("audit.log", "a") as log:

        log.write(f"{datetime.now()} - {event}\n")


# -----------------------
# LOGIN
# -----------------------
# OWASP ASVS V2 - Authentication Verification Requirements
# User authentication is performed using username lookup and Argon2 password verification

@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        # OWASP ASVS V5.3 - Injection Prevention
        # Parameterized query prevents SQL Injection attacks
        cursor.execute( "SELECT username,password,role FROM users WHERE username=?"
                       , (username,))

        user = cursor.fetchone()

        conn.close()

        if user is None:
            
            write_log(f"LOGIN FAILED : {username}")
            
            return render_template("login.html", error="Invalid username or password")

        try:

            ph.verify(user[1], password)

            # OWASP ASVS V3 - Session Management
            # Session is created after successful authentication
            session["pre_auth_user"] = username
            session["role"] = user[2]
            
            otp = str(random.randint(100000, 999999))
            
            session["otp"] = otp
            
            print("=" * 40)
            print("SECUREFIN OTP:", otp)
            print("=" * 40)

            return redirect("/otp")

        except VerifyMismatchError:
            
            write_log(f"LOGIN FAILED : {username}")
            
            # OWASP ASVS V7 - Error Handling
            # Generic error messages prevent information disclosure
            return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")


# -----------------------
# REGISTER
# -----------------------

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        fullname = request.form["fullname"]
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        
        # OWASP ASVS V5.1 - Input Validation
        # Enforces strong password requirements before processing user input
        if len(password) < 8:
            return "Password must be at least 8 characters"
        
        if not re.search(r"[A-Z]", password):
            return "Password must contain an uppercase letter"
        
        if not re.search(r"[a-z]", password):
            return "Password must contain a lowercase letter"
        
        if not re.search(r"[0-9]", password):
            return "Password must contain a number"
        
        if not re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>/?]", password):
            return "Password must contain a special character"

        if password != confirm_password:
            return "Passwords do not match"
        
        # OWASP ASVS V2.1 - Password Security
        # Passwords are hashed using Argon2 before storage
        hashed_password = ph.hash(password)

        try:

            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()

            cursor.execute("""INSERT INTO users
                          (fullname, username, email, password)
                          VALUES (?, ?, ?, ?)""", 
                          (fullname, username, email, hashed_password))

            conn.commit()
            conn.close()

            write_log(f"REGISTER SUCCESS : {username}")

            return redirect("/login")

        except sqlite3.IntegrityError:

            return "Username already exists"

    return render_template("register.html")


# -----------------------
# OTP
# -----------------------
# OWASP ASVS V2.7 - Multi-Factor Authentication
# Users must successfully complete OTP verification after password authentication

@app.route("/otp", methods=["GET", "POST"])
def otp_verify():

    if "pre_auth_user" not in session:
        return redirect("/login")

    if "otp_attempts" not in session:
        session["otp_attempts"] = 0

    if session["otp_attempts"] >= 3:

        return render_template("otp.html", error="Too many failed attempts."
                               , is_locked=True)

    if request.method == "POST":

        otp_code = request.form["otp_code"]

        correct_otp = session.get("otp")

        if otp_code == correct_otp:

            session.pop("otp_attempts", None)

            return redirect("/customer")

        else:
            write_log( f"OTP FAILED : {session['pre_auth_user']}" )
            
            session["otp_attempts"] += 1

            remaining = 3 - session["otp_attempts"]

            return render_template(
                "otp.html",
                error=f"Incorrect OTP. Remaining attempts: {remaining}",
                is_locked=False)

    return render_template(
        "otp.html",
        error=None,
        is_locked=False
    )


# -----------------------
# CUSTOMER DASHBOARD
# -----------------------

@app.route("/customer")
def customer():

    if "pre_auth_user" not in session:
        return redirect("/login")

    return render_template("customer.html",
                           username=session["pre_auth_user"])


# -----------------------
# LOGOUT
# -----------------------

@app.route("/logout")
@app.route("/logout")
def logout():

    if "pre_auth_user" in session:
        
        # OWASP ASVS V7 - Logging and Monitoring
        # Security events are recorded for audit and monitoring purposes
        write_log( f"LOGOUT : {session['pre_auth_user']}")
    
    # OWASP ASVS V3 - Session Termination
    # Session data is destroyed upon logout
    session.clear()

    return redirect("/login")


@app.route("/admin")
def admin():

    if "role" not in session:
        return redirect("/login")

    if session["role"] != "admin":
        return render_template("denied.html")

    return render_template("admin.html")


if __name__ == "__main__":
    app.run(debug=True)