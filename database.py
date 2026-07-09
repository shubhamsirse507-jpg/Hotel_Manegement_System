import sqlite3

def get_connection():
    conn = sqlite3.connect("hotel.db")
    return conn


conn = get_connection()
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    username TEXT,
    password TEXT,
    role TEXT
)
""")

cursor.execute("SELECT * FROM users")
print(cursor.fetchall())

if cursor.fetchone() is None:
    cursor.execute("INSERT INTO users VALUES('admin','admin123','admin')")
    cursor.execute("INSERT INTO users VALUES('manager','manager123','manager')")
    cursor.execute("INSERT INTO users VALUES('reception','reception123','reception')")
    conn.commit()

cursor.close()
conn.close()