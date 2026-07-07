import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Shubham@1978",
        database="hotel_management"
    )
print("Db connected")