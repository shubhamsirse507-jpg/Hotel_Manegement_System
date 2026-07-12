"""
db.py — Shared MySQL connection module for the Hotel Management System.

Every other module (Rooms.py, ROOMBOOKING.py, bill.py, Service_re.py,
staff-reports.py, authentication.py, main.py, ...) should import
get_connection() from here instead of opening its own connection.
This keeps a single, consistent place to change host/credentials.
"""

import sys
import mysql.connector
from mysql.connector import Error

# ---------------------------------------------------------------------------
# Connection settings
# ---------------------------------------------------------------------------
# These values come straight from your phpMyAdmin screen:
#   Server:   sql12.freesqldatabase.com   (top of the phpMyAdmin page)
#   Database: sql12832782                 (top of the phpMyAdmin page)
#   Port:     3306                        (default for freesqldatabase.com)
#
# DB_USER / DB_PASSWORD are NOT visible in a screenshot for security reasons —
# freesqldatabase.com emailed them to you when you created the database
# (and they're also shown once on the site's "database created" page).
# Fill them in below.
DB_CONFIG = {
    "host": "sql12.freesqldatabase.com",
    "port": 3306,
    "user": "sql12832782",        # <-- replace if your username differs
    "password": "ypxHYNxUHt",  # <-- put your real password here
    "database": "sql12832782",
}


def get_connection():
    """
    Open and return a new MySQL connection using DB_CONFIG.
    Raises the underlying mysql.connector Error if the connection fails,
    after printing a readable message — callers can catch it if they
    want to handle it differently (e.g. show a GUI error dialog).
    """
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"[db.py] Could not connect to MySQL: {e}", file=sys.stderr)
        raise


def get_cursor(conn, dictionary=True):
    """
    Convenience helper: returns a cursor from an existing connection.
    dictionary=True makes rows come back as {'column_name': value, ...}
    instead of plain tuples — usually easier to work with in this project.
    """
    return conn.cursor(dictionary=dictionary)


def close_connection(conn):
    """Safely close a connection if it's open."""
    if conn is not None and conn.is_connected():
        conn.close()


if __name__ == "__main__":
    # Quick manual test: run `python db.py` to check the connection
    # and list the tables phpMyAdmin showed you (billing, bookings,
    # guests, housekeeping, rooms, service_requests, staff, users).
    try:
        connection = get_connection()
        cursor = get_cursor(connection, dictionary=False)
        cursor.execute("SHOW TABLES;")
        tables = [row[0] for row in cursor.fetchall()]
        print("Connected successfully. Tables found:")
        for t in tables:
            print(f"  - {t}")
        cursor.close()
        close_connection(connection)
    except Error:
        print("Connection test failed — check DB_CONFIG values above.")