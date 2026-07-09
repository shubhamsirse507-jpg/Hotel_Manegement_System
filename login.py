from tkinter import *
from tkinter import messagebox

def login():
    username = txt_username.get()
    password = txt_password.get()

    if username == "admin" and password == "admin123":
        messagebox.showinfo("Login", "Welcome Admin")
        root.destroy()
        import dashboard

    elif username == "manager" and password == "manager123":
        messagebox.showinfo("Login", "Welcome Manager")
        root.destroy()
        import dashboard

    elif username == "reception" and password == "reception123":
        messagebox.showinfo("Login", "Welcome Receptionist")
        root.destroy()
        import dashboard

    else:
        messagebox.showerror("Error", "Invalid Username or Password")

root = Tk()
root.title("Hotel Management System")
root.geometry("450x350")
root.configure(bg="lightblue")

Label(root, text="HOTEL MANAGEMENT SYSTEM",
      font=("Arial", 18, "bold"),
      bg="lightblue",
      fg="darkblue").pack(pady=20)

Label(root, text="Username",
      bg="lightblue",
      font=("Arial", 12)).pack()

txt_username = Entry(root, width=30, font=("Arial", 12))
txt_username.pack(pady=5)

Label(root, text="Password",
      bg="lightblue",
      font=("Arial", 12)).pack()

txt_password = Entry(root, width=30, show="*", font=("Arial", 12))
txt_password.pack(pady=5)

# Login Button at the bottom
Button(root,
       text="Login",
       font=("Arial", 12, "bold"),
       bg="green",
       fg="white",
       width=15,
       command=login).pack(side=BOTTOM, pady=20)

root.mainloop()