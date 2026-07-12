from database import get_connection
import database

conn = get_connection()
cursor = conn.cursor()

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

        if role == "Admin" and password == "Admin123":
            print("Login Successful")
            print("Welcome Admin")

        elif role == "Manager" and password == "Manager123":
            print("Login Successful")
            print("Welcome Manager")

        elif role == "Reception" and password == "Reception123":
            print("Login Successful")
            print("Welcome Reception")

        else:
            print("Invalid Role")

    else:
        print("Invalid Username or Password")

    cursor.close()
    conn.close()

login()

import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        connection = mysql.connector.connect(
            host="sql12.freesqldatabase.com",
            user="sql12832782",          # freesqldatabase.com uses same name as DB for username
            password="ypxHYNxUHt",    # the password you were given when the DB was created
            database="sql12832782",
            port=3306
        )
        return connection
    except Error as e:
        print(f"Database connection failed: {e}")
        return None