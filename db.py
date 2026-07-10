import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Shubham@1978",
        database="hms_db"
    )
print("Db connected")
