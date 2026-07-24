import smtplib
from email.message import EmailMessage
from reportlab.pdfgen import canvas

bills = {}

# ---------------- PDF Function ----------------

def generate_pdf(bill_id, data):

    pdf = canvas.Canvas(f"Bill_{bill_id}.pdf")

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(180, 800, "HOTEL BILL RECEIPT")

    pdf.setFont("Helvetica", 12)

    pdf.drawString(50, 760, f"Bill ID : {bill_id}")
    pdf.drawString(50, 740, f"Date : {data['Date']}")
    pdf.drawString(50, 720, f"Guest Name : {data['Guest']}")
    pdf.drawString(50, 700, f"Email : {data['Email']}")
    pdf.drawString(50, 680, f"Room Number : {data['Room']}")
    pdf.drawString(50, 660, f"Room Charges : Rs. {data['Room Charge']}")
    pdf.drawString(50, 640, f"Extra Charges : Rs. {data['Extra Charge']}")
    pdf.drawString(50, 620, f"Total Amount : Rs. {data['Total']}")
    pdf.drawString(50, 600, f"Payment Method : {data['Payment Method']}")
    pdf.drawString(50, 580, f"Payment Status : {data['Payment Status']}")

    pdf.drawString(50, 540, "Thank You For Visiting Our Hotel!")

    pdf.save()

    print(f"PDF Bill Saved Successfully : Bill_{bill_id}.pdf")


# ---------------- Email Function ----------------

def send_receipt(email, bill_id, guest, total):

    sender_email = "kamblesahil259@gmail.com"
    app_password = "hxjd dqjg hwwp bcdy"

    msg = EmailMessage()

    msg["Subject"] = "Hotel Bill Receipt"
    msg["From"] = sender_email
    msg["To"] = email

    msg.set_content(f"""
Hotel Management System

Bill Receipt

Bill ID : {bill_id}
Guest Name : {guest}
Total Amount : Rs. {total}

Thank You For Visiting Our Hotel.
""")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
            smtp.login(sender_email,app_password)
            smtp.send_message(msg)

        print("Receipt Sent Successfully.")

    except Exception as e:
        print("Email Error :",e)

while True:

    print("\n===== Billing and Payment Module =====")
    print("1. Create Bill")
    print("2. View Bills")
    print("3. Payment")
    print("4. Search Bill")
    print("5. Update Bill")
    print("6. Delete Bill")
    print("7. Exit")

    choice=input("Enter Your Choice : ")

    if choice=="1":

        date=input("Enter Date (YYYY-MM-DD): ")
        bill_id=input("Enter Bill ID: ")
        guest=input("Enter Guest Name: ")
        email=input("Enter Guest Email: ")
        room=input("Enter Room Number: ")

        room_charge=float(input("Enter Room Charges: "))
        extra_charge=float(input("Enter Extra Service Charges: "))

        total=room_charge+extra_charge

        bills[bill_id]={
            "Date":date,
            "Guest":guest,
            "Email":email,
            "Room":room,
            "Room Charge":room_charge,
            "Extra Charge":extra_charge,
            "Total":total,
            "Payment Method":"Not Paid",
            "Payment Status":"Pending"
        }

        print("Bill Created Successfully!")
        print("Total Amount =",total)

    elif choice=="2":

        if len(bills)==0:
            print("No Bills Found.")
        else:
            for bill_id,data in bills.items():

                print("\n----------------------------")
                print("Bill ID :",bill_id)

                for key,value in data.items():
                    print(key,":",value)

    elif choice=="3":

        bill_id=input("Enter Bill ID : ")

        if bill_id in bills:

            print("\nPayment Method")
            print("1. Cash")
            print("2. Card")
            print("3. UPI")

            method=input("Select Payment Method : ")

            if method=="1":
                payment="Cash"
            elif method=="2":
                payment="Card"
            elif method=="3":
                payment="UPI"
            else:
                payment="Unknown"

            bills[bill_id]["Payment Method"]=payment
            bills[bill_id]["Payment Status"]="Paid"

            print("Payment Successful!")
            print("Receipt Generated Successfully!")

            generate_pdf(bill_id,bills[bill_id])

            send_receipt(
                bills[bill_id]["Email"],
                bill_id,
                bills[bill_id]["Guest"],
                bills[bill_id]["Total"]
            )

        else:
            print("Bill Not Found!")

    elif choice=="4":

        search=input("Enter Bill ID or Guest Name : ")

        found=False

        for bill_id,data in bills.items():

            if bill_id==search or data["Guest"].lower()==search.lower():

                print("\nBill ID :",bill_id)

                for key,value in data.items():
                    print(key,":",value)

                found=True

        if not found:
            print("Bill Not Found!")

    elif choice=="5":

        bill_id=input("Enter Bill ID : ")

        if bill_id in bills:

            room_charge=float(input("Enter New Room Charge : "))
            extra_charge=float(input("Enter New Extra Charge : "))

            bills[bill_id]["Room Charge"]=room_charge
            bills[bill_id]["Extra Charge"]=extra_charge
            bills[bill_id]["Total"]=room_charge+extra_charge

            print("Bill Updated Successfully!")

        else:
            print("Bill Not Found!")

    elif choice=="6":

        bill_id=input("Enter Bill ID : ")

        if bill_id in bills:

            del bills[bill_id]

            print("Bill Deleted Successfully!")

        else:
            print("Bill Not Found!")

    elif choice=="7":

        print("Thank You!")
        break

    else:

        print("Invalid Choice!")
