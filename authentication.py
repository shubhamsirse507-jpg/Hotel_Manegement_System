from database import get_connection
import database

def login():

    username = input("Enter Username: ")
    password = input("Enter Password: ")

    conn = database.get_connection()
    cursor = conn.cursor()

    query = """
    SELECT role
    FROM users
    WHERE username = ? AND password = ?
    """

    cursor.execute(query, (username, password))

    result = cursor.fetchone()

    if result:
        role = result[0]

        if role == "admin" and password == "admin123":
            print("Login Successful")
            print("Welcome Admin")

        elif role == "manager" and password == "manager123":
            print("Login Successful")
            print("Welcome Manager")

        elif role == "reception" and password == "reception123":
            print("Login Successful")
            print("Welcome Reception")

        else:
            print("Invalid Role")

    else:
        print("Invalid Username or Password")

    cursor.close()
    conn.close()

login()