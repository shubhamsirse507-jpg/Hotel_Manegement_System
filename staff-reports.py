from db import get_connection
from Rooms import show_rooms, get_room_numbers

def add_staff():
    name = input("Full Name: ")
    designation = input("Designation (Manager/Receptionist/Housekeeping/Chef/Security): ")
    phone = input("Phone: ")
    email = input("Email: ")
    salary = input("Salary: ")
    joining_date = input("Joining Date (YYYY-MM-DD): ")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO staff(full_name,designation,phone,email,salary,joining_date) VALUES(%s,%s,%s,%s,%s,%s)",
        (name, designation, phone, email, salary, joining_date),
    )

    conn.commit()
    conn.close()

    print("Staff Added Successfully\n")


def show_staff():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM staff")
    rows = cursor.fetchall()

    conn.close()

    if not rows:
        print("No staff records found.\n")
        return

    print(f"{'ID':<5}{'Name':<20}{'Designation':<15}{'Phone':<15}{'Email':<25}{'Salary':<10}{'Joining Date':<12}")
    print("-" * 100)
    for row in rows:
        print(f"{row[0]:<5}{row[1]:<20}{row[2]:<15}{row[3]:<15}{row[4]:<25}{str(row[5]):<10}{str(row[6]):<12}")
    print()


def update_staff():
    staff_id = input("Enter Staff ID to update: ")

    print("Leave a field blank to keep it unchanged.")
    name = input("Full Name: ")
    designation = input("Designation: ")
    phone = input("Phone: ")
    email = input("Email: ")
    salary = input("Salary: ")
    joining_date = input("Joining Date (YYYY-MM-DD): ")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM staff WHERE staff_id= %s", (staff_id,))
    existing = cursor.fetchone()

    if not existing:
        print("Staff ID not found.\n")
        conn.close()
        return

    cursor.execute("""
    UPDATE staff
    SET full_name=%s,designation=%s,phone=%s,email=%s,salary=%s,joining_date=%s
    WHERE staff_id=%s
    """,
    (   
        name or existing[1],
        designation or existing[2],
        phone or existing[3],
        email or existing[4],
        salary or existing[5],
        joining_date or existing[6],
        staff_id 

    ))

    conn.commit()
    conn.close()

    print("Updated Successfully\n")


def delete_staff():
    staff_id = input("Enter Staff ID to delete: ")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM staff WHERE staff_id=%s", (staff_id,))

    conn.commit()
    conn.close()

    print("Staff Deleted Successfully\n")


# ================= Housekeeping =================

def assign_room():
    room_numbers = get_room_numbers()

    if not room_numbers:
        print("No rooms found. Please add a room first.\n")
        return

    print("Available Rooms:", ", ".join(str(r) for r in room_numbers))
    room = input("Room No: ")

    if room not in [str(r) for r in room_numbers]:
        print("Invalid Room No. Please choose from the list above.\n")
        return

    assign = input("Assign Staff: ")
    status = input("Status (Clean/Dirty/In Progress): ")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO housekeeping (room_no, assigned_staff, status)
    VALUES (%s,%s,%s)
    ON DUPLICATE KEY UPDATE
        assigned_staff = VALUES(assigned_staff),
        status = VALUES(status)
    """,
    (room, assign, status))

    conn.commit()
    conn.close()

    print("Room Assigned\n")


def show_housekeeping():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM housekeeping")
    rows = cursor.fetchall()

    conn.close()

    if not rows:
        print("No housekeeping records found.\n")
        return

    print(f"{'Room No':<10}{'Assigned Staff':<20}{'Status':<15}")
    print("-" * 45)
    for row in rows:
        print(f"{row[0]:<10}{row[1]:<20}{row[2]:<15}")
    print()


# ================= Menu =================

def main_menu():
    while True:
        print("===== Staff & Housekeeping Management =====")
        print("1. Add Staff")
        print("2. View Staff")
        print("3. Update Staff")
        print("4. Delete Staff")
        print("5. Assign Room (Housekeeping)")
        print("6. View Housekeeping")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_staff()
        elif choice == "2":
            show_staff()
        elif choice == "3":
            update_staff()
        elif choice == "4":
            delete_staff()
        elif choice == "5":
            assign_room()
        elif choice == "6":
            show_housekeeping()
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.\n")


if __name__ == "__main__":
    main_menu()