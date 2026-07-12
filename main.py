"""
main.py
=======
Central entry point for the Hotel Management System.

NONE of the teammate-written files (authentication.py, bill.py,
ROOMBOOKING (1).py, Rooms.py, Service_re.py, staff-reports.py) are
modified. Every fix needed to wire them together lives in this file only.

WHY THIS IS NEEDED
-------------------
Several of those files can't be used with a normal `import` statement as-is:

1. bill.py and "ROOMBOOKING (1).py" both have their interactive menu
   (`while True: ...`) sitting as bare top-level code, not guarded by
   `if __name__ == "__main__":`. A plain `import bill` would immediately
   launch bill.py's own menu loop instead of just giving us its functions.

2. authentication.py calls `login()` unconditionally at the bottom of the
   file, and login() only prints the result - it never returns the role.
   A plain `import authentication` would immediately launch its login
   prompt with no way for this file to find out which role logged in.

3. "ROOMBOOKING (1).py" and "staff-reports.py" have spaces/parentheses/
   hyphens in their filenames, which are not valid in a Python
   `import module_name` statement.

HOW THIS FILE FIXES IT (without editing any of those files)
-------------------------------------------------------------
`load_module()` below reads a teammate's .py file as text, parses it with
the `ast` module, and only keeps their `import` statements and function/
class definitions - it drops any bare top-level statements (their menu
loops, their trailing `login()` call). It then executes just that filtered
code into its own private namespace and hands back an object exposing
their functions, e.g. `bill_mod.create_bill()`.

Because we work from the file path directly, filenames with spaces or
hyphens are no problem either.

For authentication.py specifically, this also means its own `login()`
function is reused exactly as written (same prompts, same fixed
per-role passwords, same messages) - we just capture what it prints so
this file can tell which role logged in, instead of duplicating any of
that logic ourselves.
"""

import ast
import contextlib
import io
import os
import sys
import types

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from db import get_connection

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# ================= Safe loader for teammate files =================

def load_module(filename, module_name, source_fixes=None):
    """
    Load only the import/function/class definitions from a teammate's
    script, skipping any bare top-level statements (menu loops, stray
    function calls, etc.) so nothing runs as a side effect of loading it.
    The original file on disk is never touched.

    `source_fixes`, if given, is a list of (old, new) string pairs applied
    to the file's text ONLY in memory, right before it's parsed/executed -
    used for small bugs (like a misspelled column name) that would
    otherwise crash a teammate's function, without ever writing anything
    back to their file on disk.
    """
    filepath = os.path.join(BASE_DIR, filename)

    with open(filepath, "r", encoding="utf-8") as f:
        source = f.read()

    if source_fixes:
        for old, new in source_fixes:
            if old not in source:
                print(f"NOTE: expected text to patch not found in {filename}: {old!r}")
                continue
            source = source.replace(old, new)

    tree = ast.parse(source, filename=filepath)

    tree.body = [
        node for node in tree.body
        if isinstance(node, (
            ast.Import, ast.ImportFrom, ast.FunctionDef, ast.ClassDef,
            ast.Assign, ast.AnnAssign,  # simple module-level constants,
                                        # e.g. bill.py's RECEIPT_DIR = "receipts"
        ))
    ]
    ast.fix_missing_locations(tree)

    module = types.ModuleType(module_name)
    module.__file__ = filepath
    # Let internal `from Rooms import ...`-style imports resolve against
    # this folder, same as if the files were run normally.
    if BASE_DIR not in sys.path:
        sys.path.insert(0, BASE_DIR)

    exec(compile(tree, filepath, "exec"), module.__dict__)
    return module


# Load every teammate module through the safe loader (their files are
# read, never modified).
auth_mod = load_module(
    "authentication.py", "authentication_safe",
    source_fixes=[
        ('role == "Reception"', 'role == "Receptionist"'),
        ('print("Welcome Reception")', 'print("Welcome Receptionist")'),
    ]
)
rooms_mod = load_module("Rooms.py", "rooms_safe")
booking_mod = load_module(
    "ROOMBOOKING (1).py", "booking_safe",
    source_fixes=[
        # search_booking() queries "gurest_name" (typo) instead of
        # "guest_name", which crashes with a MySQL "Unknown column" error.
        # Fixed in memory only - ROOMBOOKING (1).py on disk is untouched.
        ('WHERE gurest_name = %s', 'WHERE guest_name = %s'),
        # cancel_booking() has a stray "6" sitting in the middle of its
        # UPDATE statement ("SET 6\n    booking_status = ..."), which
        # breaks the SQL syntax. Fixed in memory only.
        ("SET 6\n    booking_status = 'Cancelled'", "SET booking_status = 'Cancelled'"),
    ],
)
bill_mod = load_module("bill.py", "bill_safe")
service_mod = load_module("Service_re.py", "service_safe")
staff_mod = load_module("staff-reports.py", "staff_safe")


# ================= Login (reuses authentication.py's own login()) =====

def _role_from_login_output(text):
    if "Welcome Admin" in text:
        return "Admin"
    if "Welcome Manager" in text:
        return "Manager"
    if "Welcome Receptionist" in text:
        return "Receptionist"
    if "Welcome Reception" in text:
        return "Reception"
    return None


class _Tee(io.TextIOBase):
    """Writes to both the real terminal and an in-memory buffer, so the
    user still sees every prompt/message live while we also capture the
    text to figure out which role just logged in."""

    def __init__(self, *streams):
        self.streams = streams

    def write(self, data):
        for s in self.streams:
            s.write(data)
        return len(data)

    def flush(self):
        for s in self.streams:
            s.flush()


def authenticate():
    """
    Calls authentication.py's own login() function, unmodified, so the
    exact login logic your teammate wrote is what actually runs. login()
    doesn't return the role, so we capture what it prints (it always
    prints "Welcome <Role>" on success) and use that to route the menu.
    Returns the role string, or None if login failed.
    """
    buffer = io.StringIO()
    real_stdout = sys.stdout
    sys.stdout = _Tee(real_stdout, buffer)
    try:
        auth_mod.login()
    except Exception as e:
        sys.stdout = real_stdout
        print(f"Login failed due to an error: {e}")
        return None
    finally:
        sys.stdout = real_stdout

    return _role_from_login_output(buffer.getvalue())


# ================= Payment + Receipt with Room No. =================
#
# Adding a Room No. line to the receipt means changing generate_receipt_pdf()
# and make_payment() - both live in bill.py, which we're keeping untouched.
# Since this is a new feature (not a one-line bug fix), it's implemented
# here as a parallel function rather than patched into bill.py's source:
# it reuses the same bill lookup/payment flow bill.py has, adds a lookup
# of the room number for the booking (bookings.room_id -> rooms.room_id ->
# rooms.room_number), and includes it on the PDF.

def get_room_no_for_booking(booking_id):
    """Look up the room number booked for a given booking_id."""
    conn = get_connection()
    if conn is None:
        return None
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT room_id FROM bookings WHERE booking_id = %s", (booking_id,))
        row = cursor.fetchone()
        if not row:
            return None
        room_ref = row[0]

        cursor.execute("SELECT room_number FROM rooms WHERE room_id = %s", (room_ref,))
        result = cursor.fetchone()
        if result:
            return result[0]

        # Fallback: booking entry isn't validated against the rooms table,
        # so it's possible a room number was typed in directly instead of
        # the room's internal ID. Try matching on room_number as a backup.
        cursor.execute("SELECT room_number FROM rooms WHERE room_number = %s", (room_ref,))
        result = cursor.fetchone()
        return result[0] if result else room_ref
    finally:
        cursor.close()
        conn.close()


def generate_receipt_pdf_with_room(bill_id, booking_id, room_no, room_charges,
                                    extra_charges, total_amount, payment_method, bill_date):
    """Same layout as bill.py's generate_receipt_pdf(), plus a Room No. line."""
    os.makedirs(bill_mod.RECEIPT_DIR, exist_ok=True)
    filepath = os.path.join(bill_mod.RECEIPT_DIR, f"receipt_{bill_id}.pdf")

    c = canvas.Canvas(filepath, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width / 2, height - 80, "Payment Receipt")

    c.setFont("Helvetica", 10)
    c.drawCentredString(width / 2, height - 100, "Hotel Billing & Payment Module")

    c.line(60, height - 115, width - 60, height - 115)

    c.setFont("Helvetica", 12)
    y = height - 150
    line_height = 22

    details = [
        ("Bill ID:", str(bill_id)),
        ("Booking ID:", str(booking_id)),
        ("Room No:", str(room_no)),
        ("Bill Date:", str(bill_date)),
        ("Room Charges:", f"{room_charges:.2f}"),
        ("Extra Service Charges:", f"{extra_charges:.2f}"),
        ("Total Amount:", f"{total_amount:.2f}"),
        ("Payment Method:", str(payment_method)),
        ("Payment Status:", "Paid"),
    ]

    for label, value in details:
        c.setFont("Helvetica-Bold", 12)
        c.drawString(80, y, label)
        c.setFont("Helvetica", 12)
        c.drawString(260, y, value)
        y -= line_height

    c.line(60, y - 10, width - 60, y - 10)

    c.setFont("Helvetica-Oblique", 10)
    c.drawCentredString(width / 2, y - 30, "Thank you for your payment!")

    c.save()
    return filepath


def make_payment_with_room():
    """Same bill lookup/payment flow as bill.py's make_payment(), but looks
    up the room number for the booking and includes it on the receipt."""
    bill_id = input("Enter Bill ID: ")

    conn = get_connection()
    if conn is None:
        print("Could not connect to database.")
        return
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM billing WHERE bill_id=%s", (bill_id,))
    data = cursor.fetchone()

    if not data:
        print("Bill Not Found!")
        cursor.close()
        conn.close()
        return

    if data[6] == "Paid":
        print("This bill is already Paid.")
        cursor.close()
        conn.close()
        return

    print("Payment Methods:")
    print("1. Cash")
    print("2. Card")
    print("3. UPI")
    method = input("Select Payment Method: ")
    payment = {"1": "Cash", "2": "Card", "3": "UPI"}.get(method, "Unknown")

    cursor.execute(
        "UPDATE billing SET payment_status=%s, payment_method=%s WHERE bill_id=%s",
        ("Paid", payment, bill_id),
    )
    conn.commit()
    cursor.close()
    conn.close()

    print("Payment Received Successfully!")

    room_no = get_room_no_for_booking(data[1])

    try:
        receipt_path = generate_receipt_pdf_with_room(
            bill_id=data[0],
            booking_id=data[1],
            room_no=room_no if room_no is not None else "N/A",
            room_charges=data[2],
            extra_charges=data[3],
            total_amount=data[4],
            payment_method=payment,
            bill_date=data[7],
        )
        print(f"Receipt Generated: {receipt_path}")
    except Exception as e:
        print("Payment recorded, but failed to generate PDF receipt:", e)


# ================= Role-based sub-menus =================

def rooms_menu(role):
    while True:
        print("\n===== Room Management =====")
        print("1. View Rooms")
        print("2. Search Rooms by Status")
        if role in ("Admin", "Manager"):
            print("3. Add Room")
            print("4. Update Room")
        if role == "Admin":
            print("5. Delete Room")
        print("0. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1":
            rooms_mod.show_rooms()
        elif choice == "2":
            rooms_mod.search_room_by_status()
        elif choice == "3" and role in ("Admin", "Manager"):
            rooms_mod.add_room()
        elif choice == "4" and role in ("Admin", "Manager"):
            rooms_mod.update_room()
        elif choice == "5" and role == "Admin":
            rooms_mod.delete_room()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")


def bookings_menu(role):
    while True:
        print("\n===== Room Booking & Check-In/Check-Out =====")
        print("1. Book Room")
        print("2. View Booking")
        print("3. Search Booking")
        print("4. Modify Booking")
        print("5. Cancel Booking")
        print("6. Guest Check-In")
        print("7. Guest Check-Out")
        print("0. Back to Main Menu")

        choice = input("Enter Your Choice: ")

        if choice == "1":
            booking_mod.book_room()
        elif choice == "2":
            booking_mod.view_booking()
        elif choice == "3":
            booking_mod.search_booking()
        elif choice == "4":
            booking_mod.modify_booking()
        elif choice == "5":
            booking_mod.cancel_booking()
        elif choice == "6":
            booking_mod.check_in()
        elif choice == "7":
            booking_mod.check_out()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")


def billing_menu(role):
    while True:
        print("\n===== Billing and Payment Module =====")
        print("1. Create Bill")
        print("2. View Bills")
        print("3. Payment")
        print("4. Search Bill")
        if role in ("Admin", "Manager"):
            print("5. Update Bill")
        if role == "Admin":
            print("6. Delete Bill")
        print("0. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1":
            bill_mod.create_bill()
        elif choice == "2":
            bill_mod.view_bills()
        elif choice == "3":
            make_payment_with_room()
        elif choice == "4":
            bill_mod.search_bill()
        elif choice == "5" and role in ("Admin", "Manager"):
            bill_mod.update_bill()
        elif choice == "6" and role == "Admin":
            bill_mod.delete_bill()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")


def service_requests_menu(role):
    while True:
        print("\n===== Service Requests =====")
        print("1. Add Service Request")
        print("2. View All Requests")
        print("3. Update Status")
        if role == "Admin":
            print("4. Delete Request")
        print("0. Back to Main Menu")

        choice = input("Choose: ").strip()

        if choice == "1":
            service_mod.add_service_request()
        elif choice == "2":
            service_mod.view_service_requests()
        elif choice == "3":
            service_mod.update_request_status()
        elif choice == "4" and role == "Admin":
            service_mod.delete_service_request()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")


def staff_menu(role):
    # Only Admin and Manager can reach this menu at all (see main_menu)
    while True:
        print("\n===== Staff & Housekeeping Management =====")
        print("1. View Staff")
        print("2. View Housekeeping")
        print("3. Assign Room (Housekeeping)")
        if role == "Admin":
            print("4. Add Staff")
            print("5. Update Staff")
            print("6. Delete Staff")
        print("0. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1":
            staff_mod.show_staff()
        elif choice == "2":
            staff_mod.show_housekeeping()
        elif choice == "3":
            staff_mod.assign_room()
        elif choice == "4" and role == "Admin":
            staff_mod.add_staff()
        elif choice == "5" and role == "Admin":
            staff_mod.update_staff()
        elif choice == "6" and role == "Admin":
            staff_mod.delete_staff()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")


# ================= Main Menu (role based) =================

def main_menu(role):
    while True:
        print(f"\n===== HOTEL MANAGEMENT SYSTEM ({role}) =====")
        print("1. Room Management")
        print("2. Room Booking / Check-In-Out")
        print("3. Billing and Payment")
        print("4. Service Requests")
        if role in ("Admin", "Manager"):
            print("5. Staff & Housekeeping")
        print("0. Logout")

        choice = input("Enter your choice: ")

        if choice == "1":
            rooms_menu(role)
        elif choice == "2":
            bookings_menu(role)
        elif choice == "3":
            billing_menu(role)
        elif choice == "4":
            service_requests_menu(role)
        elif choice == "5" and role in ("Admin", "Manager"):
            staff_menu(role)
        elif choice == "0":
            print("Logged out. Goodbye!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    user_role = authenticate()
    if user_role:
        main_menu(user_role)