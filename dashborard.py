from tkinter import *
from tkinter import messagebox

def logout():
    messagebox.showinfo("Logout","Logged Out Successfully")
    root.destroy()
    import login

root = Tk()
root.title("Dashboard")
root.geometry("600x450")
root.configure(bg="white")

Label(root,
      text="HOTEL MANAGEMENT DASHBOARD",
      font=("Arial",18,"bold"),
      bg="white").pack(pady=20)

Button(root,text="Check In",width=20).pack(pady=5)
Button(root,text="Check Out",width=20).pack(pady=5)
Button(root,text="Room Booking",width=20).pack(pady=5)
Button(root,text="Billing",width=20).pack(pady=5)
Button(root,text="Customer Details",width=20).pack(pady=5)

Button(root,
       text="Logout",
       width=20,
       bg="red",
       fg="white",
       command=logout).pack(pady=20)

root.mainloop()