"""
cli/authentication.py
=====================
Authentication module for the Hotel Management System CLI.
Handles login with role-based password verification and password recovery.

login() returns the role string ("Admin" / "Manager" / "Receptionist")
on success, or None on failure — so callers can route without stdout
capturing.

The interactive menu is guarded by `if __name__ == "__main__":` so
this module can be safely imported without launching a prompt loop.
"""

import smtplib
import random
from email.mime.text import MIMEText

import os
import sys

# Ensure parent directory (project root) is in sys.path so `import db` succeeds when run directly
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from db import get_connection

# Expected passwords per role (plaintext — matches the existing users table).
_ROLE_PASSWORDS = {
    "Admin":        "admin123",
    "Manager":      "manager123",
    "Receptionist": "reception123",
    "Reception":    "reception123",   # backward-compat alias
}

# Global OTP variable
otp = None


def login():
    """
    Authenticate a user against the `users` table.

    Prints a welcome message on success and returns the canonical role
    string. Returns None on any failure.
    """
    username = input("Enter Username : ").strip()
    password = input("Enter Password : ").strip()

    conn   = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT role FROM users WHERE username = %s AND password = %s",
            (username, password),
        )
        result = cursor.fetchone()

        if not result:
            print("Invalid Username or Password")
            return None

        role = result[0]
        expected_password = _ROLE_PASSWORDS.get(role)

        if expected_password and password == expected_password:
            # Normalise "Reception" → "Receptionist" for consistent routing
            canonical = "Receptionist" if role == "Reception" else role
            print("Login Successful")
            print(f"Welcome {canonical}")
            return canonical
        else:
            print("Invalid Role or Password")
            return None

    except Exception as e:
        print(f"Login error: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def send_otp(email):
    """
    Generates a 6-digit OTP and sends it to the provided email address via SMTP.
    Displays a messagebox notification and returns the OTP on success.
    """
    global otp
    otp = str(random.randint(100000, 999999))

    sender_email = "amozon2650@gmail.com"
    sender_password = "elcv szvk wtqf ptyf"

    subject = "Password Reset OTP"
    body = f"Your OTP is: {otp}"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = email

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email, msg.as_string())
        server.quit()

        print("OTP sent to your email.")
        return otp

    except Exception as e:
        print(f"Error sending OTP: {e}")
        return None


def forgot_password():
    """
    Handles the password reset flow using OTP verification sent via email.
    """
    username = input("Enter Username: ").strip()

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT email FROM users WHERE username=%s", (username,))
        result = cursor.fetchone()

        if not result:
            print("Username not found.")
            return

        email = result[0]
        if not email:
            print("No email address found for this user.")
            return

        sent_otp = send_otp(email)
        if not sent_otp:
            print("otp could not be sent.")
            return

        user_otp = input("Enter OTP sent to your email: ").strip()

        if user_otp != sent_otp:
            print("Invalid OTP")
            return

        new_password = input("Enter New Password: ").strip()

        cursor.execute(
            "UPDATE users SET password=%s WHERE username=%s",
            (new_password, username)
        )
        conn.commit()

        print("Password updated successfully.")

    except Exception as e:
        print(f"Forgot password error: {e}")
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    print("1. Login")
    print("2. Forgot Password")

    choice = input("Enter choice: ").strip()

    if choice == "1":
        role = login()
        if role:
            print(f"Logged in as: {role}")

    elif choice == "2":
        forgot_password()