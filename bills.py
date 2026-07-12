bills = {}

while True:
    print("\n===== Billing and Payment Module =====")
    print("1. Create Bill")
    print("2. View Bills")
    print("3. Payment")
    print("4. Search Bill")
    print("5. Update Bill")
    print("6. Delete Bill")
    print("7. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        date=input("Enter (YYYY-MM-DD): ")
        bill_id = input("Enter Bill ID: ")
        guest = input("Enter Guest Name: ")
        room = input("Enter Room Number: ")

        room_charge = float(input("Enter Room Charges: "))
        extra_charge = float(input("Enter Extra Service Charges: "))

        total = room_charge + extra_charge

        bills[bill_id] = {
            "Guest": guest,
            "Room": room,
            "Room Charge": room_charge,
        
            "Extra Charge": extra_charge,
            "Total": total,
            "Payment Status": "Pending"
        }

        print("Bill Created Successfully!")
        print("Total Amount =", total)

    elif choice == "2":
        if len(bills) == 0:
            print("No Bills Found.")
        else:
            for bill_id, data in bills.items():
                print("\nBill ID:", bill_id)
                for key, value in data.items():
                    print(key, ":", value)

    elif choice == "3":
        bill_id = input("Enter Bill ID: ")

        if bill_id in bills:
            print("Payment Methods:")
            print("1. Cash")
            print("2. Card")
            print("3. UPI")

            method = input("Select Payment Method: ")

            if method == "1":
                payment = "Cash"
            elif method == "2":
                payment = "Card"
            elif method == "3":
                payment = "UPI"
            else:
                payment = "Unknown"

            bills[bill_id]["Payment Method"] = payment
            bills[bill_id]["Payment Status"] = "Paid"

            print("Payment Received Successfully!")
            print("Receipt Generated")
        else:
            print("Bill Not Found!")

    elif choice == "4":
        search = input("Enter Bill ID or Guest Name: ")

        found = False
        for bill_id, data in bills.items():
            if bill_id == search or data["Guest"].lower() == search.lower():
                print("\nBill ID:", bill_id)
                for key, value in data.items():
                    print(key, ":", value)
                found = True

        if not found:
            print("Bill Not Found!")

    elif choice == "5":
        bill_id = input("Enter Bill ID: ")

        if bill_id in bills:
            room_charge = float(input("Enter New Room Charge: "))
            extra_charge = float(input("Enter New Extra Charge: "))

            bills[bill_id]["Room Charge"] = room_charge
            bills[bill_id]["Extra Charge"] = extra_charge
            bills[bill_id]["Total"] = room_charge + extra_charge

            print("Bill Updated Successfully!")
        else:
            print("Bill Not Found!")

    elif choice == "6":
        bill_id = input("Enter Bill ID: ")

        if bill_id in bills:
            del bills[bill_id]
            print("Bill Deleted Successfully!")
        else:
            print("Bill Not Found!")

    elif choice == "7":
        print("Thank You!")
        break

    else:
        print("Invalid Choice!")