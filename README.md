# SecureFin User Authentication Application

## Overview

SecureFin is a secure user authentication web application developed using Python Flask. The system demonstrates secure coding practices by implementing user registration, authentication, multi-factor authentication (MFA), session management, role-based access control (RBAC), password hashing, and audit logging.

The project was developed as part of the Secure Software Systems coursework to demonstrate compliance with secure coding principles and OWASP ASVS requirements.

---

## Features

* User Registration
* Secure Login Authentication
* Password Hashing using Argon2
* Multi-Factor Authentication (OTP)
* Session Management
* Role-Based Access Control (RBAC)
* Audit Logging
* Input Validation
* SQL Injection Prevention using Parameterized Queries

---

## Technologies Used

* Python 3
* Flask
* SQLite3
* Argon2 Password Hasher
* HTML5
* CSS3
* Bootstrap 5

---

## Installation

Install required packages:

pip install -r requirements.txt

---

## Database Setup

Run the following script to create the SQLite database:

python create_db.py

This will generate:

users.db

---

## Running the Application

Start the Flask application:

python app.py

Open the browser and visit:

http://127.0.0.1:5000

---

## Default OTP Behaviour

A random six-digit OTP is generated after successful login and displayed in the terminal for demonstration purposes.

---

## Security Controls Implemented

1. Input Validation
2. Secure Password Storage (Argon2)
3. Parameterized Queries
4. Multi-Factor Authentication (OTP)
5. Session Management
6. Role-Based Access Control
7. Secure Error Handling
8. Audit Logging

---

## Project Structure

SecureFin/

├── app.py

├── create_db.py

├── users.db

├── audit.log

├── requirements.txt

├── README.md

├── templates/

│   ├── login.html

│   ├── register.html

│   ├── otp.html

│   ├── customer.html

│   ├── admin.html

│   └── denied.html

└── static/

```
├── css/

│   └── style.css

└── images/

    └── logo.png
```
