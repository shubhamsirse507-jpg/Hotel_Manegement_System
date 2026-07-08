from tkinter import *
from tkinter import messagebox
import auth

# =====================================================
# 1.3.1 Login Screen
# On success, closes this window and launches the dashboard.
# =====================================================

root = Tk()
root.title("Hotel Management System - Login")
root.geometry("420x420")
root.config(bg="#ECF0F1")
root.resizable(False, False)

HEADER = "#2C3E50"
BUTTON = "#34495E"

# --- Header banner
header = Frame(root, bg=HEADER, height=90)
header.pack(fill=X)

Label(
    header,
    text="HOTEL MANAGEMENT\nSYSTEM",
    bg=HEADER,
    fg="white",
    font=("Arial", 16, "bold"),
    justify="center"
).pack(pady=15)

# --- Login form
form = Frame(root, bg="#ECF0F1")
form.pack(pady=40)

Label(form, text="Username", bg="#ECF0F1", font=("Arial", 12)).grid(row=0, column=0, sticky="w", pady=8)
username_entry = Entry(form, width=28, font=("Arial", 12))
username_entry.grid(row=1, column=0, pady=(0, 15))

Label(form, text="Password", bg="#ECF0F1", font=("Arial", 12)).grid(row=2, column=0, sticky="w", pady=8)
password_entry = Entry(form, width=28, font=("Arial", 12), show="*")
password_entry.grid(row=3, column=0, pady=(0, 15))

status_label = Label(root, text="", bg="#ECF0F1", fg="red", font=("Arial", 10))
status_label.pack()


def attempt_login():
    username = username_entry.get().strip()
    password = password_entry.get().strip()

    if not username or not password:
        status_label.config(text="Please enter both username and password.")
        return

    user = auth.authenticate(username, password)

    if user:
        messagebox.showinfo("Welcome", f"Logged in as {user['username']} ({user['role']})")
        root.destroy()
        launch_dashboard()
    else:
        status_label.config(text="Invalid username or password.")
        password_entry.delete(0, "end")


def launch_dashboard():
    # Import here (not at top) so the dashboard module only
    # loads/opens its own Tk window AFTER login succeeds.
    import gui_dashboard  # noqa: F401  (dashboard.py runs its own mainloop on import)


Button(
    root, text="Login", width=20, bg=BUTTON, fg="white",
    font=("Arial", 12, "bold"), relief="flat",
    command=attempt_login
).pack(pady=10)

# allow pressing Enter to log in
root.bind("<Return>", lambda event: attempt_login())

root.mainloop()