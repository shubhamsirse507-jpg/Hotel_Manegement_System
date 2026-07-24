from db import get_connection


def add_guest():

    full_name = input("Enter Guest Full_Name: ")
    gender = input("Enter Your Gender")
    phone = input("Enter Contact Number: ")
    email = input("Enter Email: ")
    address = input("Enter Address: ")
    id_proof = input("Enter ID Proof Type: ")
    proof_number = input("Enter ID Proof Number: ")

    # Validation
    if not (phone.isdigit() and len(phone) == 10):
        print("Invalid Phone Number! Please enter a valid phone number.")
        return

    if not (proof_number.isdigit() and len(proof_number) == 12):
        print("Invalid ID Proof Number! Please enter a valid ID Proof Number.")
        return

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO guests
    (full_name,gender,number,email,address,id_proof,id_proof_number)
    VALUES (%s,%s,%s,%s,%s,%s)
    """

    cursor.execute(query,
                   (name, phone, email, address, proof_type, proof_number))

    conn.commit()

    cursor.close()
    conn.close()

    print("Guest Added Successfully!")


def view_guest():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM guests")

    records = cursor.fetchall()

    if len(records) == 0:
        print("No Guest Records Found.")

    else:
        print("\n===== Guest List =====")

        for data in records:
            print("Guest ID :", data[0])
            print("Name     :", data[1])
            print("Phone    :", data[2])
            print("Email    :", data[3])
            print("Address  :", data[4])
            print("ID Proof :", data[5])
            print("Proof No :", data[6])
            print("----------------------------")

    cursor.close()
    conn.close()


def search_guest():

    guest_id = input("Enter Guest ID to Search: ")

    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM guests WHERE guest_id=%s"

    cursor.execute(query, (guest_id,))

    data = cursor.fetchone()

    if data:
        print("\nGuest Found")
        print("Guest ID :", data[0])
        print("Name     :", data[1])
        print("Phone    :", data[2])
        print("Email    :", data[3])
        print("Address  :", data[4])

    else:
        print("Guest Not Found.")

    cursor.close()
    conn.close()
def update_guest():

    guest_id = input("Enter Guest ID to Update: ")

    name = input("New Name: ")
    phone = input("New Phone: ")
    email = input("New Email: ")
    address = input("New Address: ")
    proof_type = input("New ID Proof Type: ")
    proof_number = input("New ID Proof Number: ")

    # Validation
    if not (phone.isdigit() and len(phone) == 10):
        print("Invalid Phone Number! Please enter a valid phone number.")
        return

    if not (proof_number.isdigit() and len(proof_number) == 12):
        print("Invalid ID Proof Number! Please enter a valid ID Proof Number.")
        return

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    UPDATE guests
    SET name=%s,
        contact_number=%s,
        email=%s,
        address=%s,
        id_proof_type=%s,
        id_proof_number=%s
    WHERE guest_id=%s
    """

    cursor.execute(query,
                   (name, phone, email, address, proof_type, proof_number, guest_id))

    conn.commit()

    if cursor.rowcount > 0:
        print("Guest Updated Successfully!")
    else:
        print("Guest ID Not Found.")

    cursor.close()
    conn.close()


def delete_guest():

    guest_id = input("Enter Guest ID to Delete: ")

    conn = get_connection()
    cursor = conn.cursor()

    query = "DELETE FROM guests WHERE guest_id=%s"

    cursor.execute(query, (guest_id,))

    conn.commit()

    if cursor.rowcount > 0:
        print("Guest Deleted Successfully!")
    else:
        print("Guest ID Not Found.")

    cursor.close()
    conn.close()


while True:

    print("\n========== GUEST MANAGEMENT SYSTEM ==========")
    print("1. Add Guest")
    print("2. View Guest")
    print("3. Search Guest")
    print("4. Update Guest")
    print("5. Delete Guest")
    print("6. Exit")

    choice = input("Enter Your Choice: ")

    if choice == "1":
        add_guest()

    elif choice == "2":
        view_guest()

    elif choice == "3":
        search_guest()

    elif choice == "4":
        update_guest()

    elif choice == "5":
        delete_guest()

    elif choice == "6":
        print("Thank You!")
        break

    else:
        print("Invalid Choice. Please Try Again.")