# authentication.py

users = {
    "admin": "admin123",
    "manager": "manager123",
    "reception": "reception123"
}

print("===== HOTEL MANAGEMENT SYSTEM LOGIN =====")

username = input("Enter Username: ")
password = input("Enter Password: ")

if username in users and users[username] == password:
    print(f"\nLogin Successful!")
    print(f"Welcome, {username.title()}!")
else:
    print("\nInvalid Username or Password!")