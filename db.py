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
