from db import get_connection

def book_room():

    customer_name = input("Enter Customer Name: ")

    print("\nSelect Room Type")
    print("1. Single Room")
    print("2. Double Room")
    print("3. Deluxe Room")

    room_choice = input("Enter Choice (1-3): ")

    if room_choice == "1":
        room_type = "Single"
    elif room_choice == "2":
        room_type = "Double"
    elif room_choice == "3":
        room_type = "Deluxe"
    else:
        print("Invalid Room Type!")
        return

    adults = int(input("Enter Number of Adults: "))
    children = int(input("Enter Number of Children: "))

    check_in = input("Enter Check-In Date (YYYY-MM-DD): ")
    check_out = input("Enter Check-Out Date (YYYY-MM-DD): ")

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO booking
    (customer_name, room_type, adults, children,
     check_in, check_out, booking_status)
    VALUES (%s,%s,%s,%s,%s,%s,%s)
    """

    cursor.execute(
        query,
        (
            customer_name,
            room_type,
            adults,
            children,
            check_in,
            check_out,
            "Booked"
        )
    )

    conn.commit()

    cursor.close()
    conn.close()

    print("Room Booked Successfully!")

def view_booking():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM booking")

    records = cursor.fetchall()

    if len(records) == 0:
        print("No Booking Records Found.")

    else:
        print("\n===== Booking Details =====")

        for data in records:

            print("Booking ID     :", data[0])
            print("Customer       :", data[1])
            print("Room Type      :", data[2])
            print("Adults         :", data[3])
            print("Children       :", data[4])
            print("Check-In       :", data[5])
            print("Check-Out      :", data[6])
            print("Booking Status :", data[7])
            print("Created At     :", data[8])
            print("-----------------------------")
    cursor.close()
    conn.close()

def search_booking():

    booking_id = input("Enter Booking ID to Search: ")

    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM booking WHERE booking_id=%s"

    cursor.execute(query, (booking_id,))

    data = cursor.fetchone()

    if data:

        print("\nBooking Found")
        print("Booking ID     :", data[0])
        print("Customer       :", data[1])
        print("Room Type      :", data[2])
        print("Adults         :", data[3])
        print("Children       :", data[4])
        print("Check-In       :", data[5])
        print("Check-Out      :", data[6])
        print("Booking Status :", data[7])
        print("Created At     :", data[8])

    else:
        print("Booking Not Found.")

    cursor.close()
    conn.close()

def modify_booking():

    booking_id = input("Enter Booking ID to Modify: ")

    print("\nSelect New Room Type")
    print("1. Single Room")
    print("2. Double Room")
    print("3. Deluxe Room")

    room_choice = input("Enter Choice (1-3): ")

    if room_choice == "1":
        room_type = "Single"

    elif room_choice == "2":
        room_type = "Double"

    elif room_choice == "3":
        room_type = "Deluxe"

    else:
        print("Invalid Room Type!")
        return
    
    adults = int(input("Enter Number of Adults: "))
    children = int(input("Enter Number of Children: "))

    check_in = input("Enter Check-In Date (YYYY-MM-DD): ")
    check_out = input("Enter Check-Out Date (YYYY-MM-DD): ")
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    UPDATE booking
    SET room_type=%s,
        adults=%s,
        children=%s,
        check_in=%s,
        check_out=%s
    WHERE booking_id=%s
    """

    cursor.execute(
        query,
        (
            room_type,
            adults,
            children,
            check_in,
            check_out,
            booking_id
        )
    )

    conn.commit()

    if cursor.rowcount > 0:
        print("Booking Modified Successfully!")
    else:
        print("Booking ID Not Found.")

    cursor.close()
    conn.close()


def cancel_booking():

    booking_id = input("Enter Booking ID to Cancel: ")

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    UPDATE booking
    SET booking_status='Cancelled'
    WHERE booking_id=%s
    """

    cursor.execute(query, (booking_id,))

    conn.commit()

    if cursor.rowcount > 0:
        print("Booking Cancelled Successfully!")
    else:
        print("Booking ID Not Found.")

    cursor.close()
    conn.close()

def check_in():

    booking_id = input("Enter Booking ID for Check-In: ")

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    UPDATE booking
    SET booking_status='Checked-In'
    WHERE booking_id=%s
    """
    cursor.execute(query, (booking_id,))

    conn.commit()

    if cursor.rowcount > 0:
        print("Guest Checked-In Successfully!")
    else:
        print("Booking ID Not Found.")

    cursor.close()
    conn.close()

def check_out():

    booking_id = input("Enter Booking ID for Check-Out: ")

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    UPDATE booking
    SET booking_status='Checked-Out'
    WHERE booking_id=%s
    """

    cursor.execute(query, (booking_id,))

    conn.commit()

    if cursor.rowcount > 0:
        print("Guest Checked-Out Successfully!")
    else:
        print("Booking ID Not Found.")

    cursor.close()
    conn.close()


while True:

    print("\n====== ROOM BOOKING & CHECK-IN/CHECK-OUT ======")
    print("1. Book Room")
    print("2. View Booking")
    print("3. Search Booking")
    print("4. Modify Booking")
    print("5. Cancel Booking")
    print("6. Guest Check-In")
    print("7. Guest Check-Out")
    print("8. Exit")

    choice = input("Enter Your Choice: ")

    if choice == "1":
        book_room()

    elif choice == "2":
        view_booking()

    elif choice == "3":
        search_booking()

    elif choice == "4":
        modify_booking()

    elif choice == "5":
        cancel_booking()

    elif choice == "6":
        check_in()

    elif choice == "7":
        check_out()

    elif choice == "8":
        print("Thank You!")
        break

    else:
        print("Invalid Choice. Please Try Again.")