# Hotel Management System (HMS) - Project Description

The **Hotel Management System (HMS)** is a dual-interface application (supporting both a Command Line Interface (CLI) and a Graphical User Interface (GUI)) powered by Python and MySQL. It is designed to manage hotel operations including room management, bookings, guest check-ins/check-outs, billing/payment processing, service requests, and staff/housekeeping management.

The system enforces role-based access control (RBAC) for three primary roles: **Admin**, **Manager**, and **Receptionist**.

---

## 🏗️ Project Architecture

```mermaid
graph TD
    db[(MySQL Database)] <--> db_py[db.py]
    
    %% GUI Interfaces
    subgraph GUI ["Tkinter GUI Interface"]
        gui_py[gui.py]
        login_py[Authentication/login.py]
    end
    
    %% CLI Interfaces
    subgraph CLI ["Console CLI Interface"]
        main_py[main.py]
        auth_py[authentication.py]
        rooms_py[Rooms.py]
        booking_py[ROOMBOOKING (1).py]
        bill_py[bill.py]
        service_py[Service_re.py]
        staff_py[staff-reports.py]
    end
    
    db_py <--> GUI
    db_py <--> CLI
    
    main_py -. Safe AST Loader .-> auth_py
    main_py -. Safe AST Loader .-> rooms_py
    main_py -. Safe AST Loader .-> booking_py
    main_py -. Safe AST Loader .-> bill_py
    main_py -. Safe AST Loader .-> service_py
    main_py -. Safe AST Loader .-> staff_py
```

### Key Integration Strategy in `main.py`
To preserve unmodified teammate files that contain raw, un-guarded `while True:` loop statements (which would normally block standard imports), [main.py](file:///d:/HMS_Project/main.py) uses a custom Abstract Syntax Tree (AST) loader (`load_module`). This loader parses the teammates' files dynamically as text, filters out bare executable statements (such as infinite loops and prompt triggers), compiles only the imports, classes, and function definitions in-memory, and injects necessary bug-fixes before launching them.

---

## 🗃️ Database Schema

The database relies on a shared connection configuration defined in [db.py](file:///d:/HMS_Project/db.py). The schema contains the following primary tables:

1. **`users`**: System login credentials.
   * `user_id` (INT, Primary Key)
   * `username` (VARCHAR)
   * `password` (VARCHAR - plaintext or hashed)
   * `role` (ENUM: `'Admin'`, `'Manager'`, `'Receptionist'`)
   * `last_login`, `created_at` (TIMESTAMPS)
2. **`rooms`**: Hotel rooms inventory.
   * `room_id` (INT, Primary Key)
   * `room_number` (VARCHAR)
   * `room_type` (ENUM: `'Single'`, `'Double'`, `'Deluxe'`, `'Suite'`)
   * `price_per_night` (DECIMAL)
   * `status` (ENUM: `'Available'`, `'Booked'`, `'Maintenance'`)
3. **`bookings`**: Room booking and guest state records.
   * `booking_id` (INT, Primary Key)
   * `guest_name`, `guest_id` (VARCHAR)
   * `room_id` (INT)
   * `check_in`, `check_out` (DATE)
   * `adults`, `children` (INT)
   * `booking_status` (ENUM: `'Confirmed'`, `'Checked In'`, `'Checked Out'`, `'Cancelled'`)
4. **`billing`**: Invoice details.
   * `bill_id` (INT, Primary Key)
   * `booking_id` (INT)
   * `room_charges`, `extra_charges`, `total_amount` (DECIMAL)
   * `payment_method` (VARCHAR: `'Cash'`, `'Card'`, `'UPI'`)
   * `payment_status` (ENUM: `'Pending'`, `'Paid'`)
   * `bill_date` (DATE)
5. **`service_requests`**: Guest amenity and utility requests.
   * `request_id` (INT, Primary Key)
   * `booking_id` (INT)
   * `service_type` (VARCHAR)
   * `details` (TEXT)
   * `status` (ENUM: `'Pending'`, `'In Progress'`, `'Completed'`, `'Cancelled'`)
6. **`staff`**: Employee metadata.
   * `staff_id` (INT, Primary Key)
   * `full_name`, `designation`, `phone`, `email` (VARCHAR)
   * `salary` (DECIMAL)
   * `joining_date` (DATE)
7. **`housekeeping`**: Cleaning/maintenance assignments.
   * `room_no` (VARCHAR, Unique Key)
   * `assigned_staff` (VARCHAR)
   * `status` (ENUM: `'Clean'`, `'Dirty'`, `'In Progress'`)

---

## 📁 File Structure & Component Map

* **📁 Root Directory**:
  * **[main.py](file:///d:/HMS_Project/main.py)**: Central entry point for CLI. Implements AST loading, in-memory patch fixes, and role-based terminal dashboards.
  * **[db.py](file:///d:/HMS_Project/db.py)**: Shared MySQL connection module.
  * **[gui.py](file:///d:/HMS_Project/gui.py)**: Complete, multi-tab Tkinter interface matching the database operations.
  * **[Rooms.py](file:///d:/HMS_Project/Rooms.py)**: Room catalog operations.
  * **[ROOMBOOKING (1).py](file:///d:/HMS_Project/ROOMBOOKING%20(1).py)**: Core booking engine, including check-in and check-out flows.
  * **[bill.py](file:///d:/HMS_Project/bill.py)**: Billing operations and PDF receipt compilation (utilizing ReportLab).
  * **[Service_re.py](file:///d:/HMS_Project/Service_re.py)**: Service request administration.
  * **[staff-reports.py](file:///d:/HMS_Project/staff-reports.py)**: Employee directory and housekeeping router.
  * **[authentication.py](file:///d:/HMS_Project/authentication.py)**: Standard plaintext authentication.
  * **[auth.py](file:///d:/HMS_Project/auth.py)**: Alternative plaintext authentication model.
  * **[check_db.py](file:///d:/HMS_Project/check_db.py)**: Diagnostic tool for DB schema inspects.

* **📁 Authentication Subdirectory (`/Authentication`)**:
  * **[login.py](file:///d:/HMS_Project/Authentication/login.py)**: GUI Login Window.
  * **[auth.py](file:///d:/HMS_Project/Authentication/auth.py)**: Session and secure bcrypt authentication layer.
  * **[Pass_hash.py](file:///d:/HMS_Project/Authentication/Pass_hash.py)**: Password hashing module.
  * **[access_control.py](file:///d:/HMS_Project/Authentication/access_control.py)**: Access control permission utility.
  * **[session.py](file:///d:/HMS_Project/Authentication/session.py)**: Tracks authenticated session state.

---

## 🔐 Role and Access Map

| Module Feature | Receptionist | Manager | Admin |
| :--- | :---: | :---: | :---: |
| **Room Management: View & Search** | Yes | Yes | Yes |
| **Room Management: Add & Update** | No | Yes | Yes |
| **Room Management: Delete** | No | No | Yes |
| **Booking: Create, Cancel, Modify, Check-in/out** | Yes | Yes | Yes |
| **Billing: Create, View, Search, Pay** | Yes | Yes | Yes |
| **Billing: Update** | No | Yes | Yes |
| **Billing: Delete** | No | No | Yes |
| **Service Requests: Add, View, Update** | Yes | Yes | Yes |
| **Service Requests: Delete** | No | No | Yes |
| **Staff & Housekeeping: View, Assign** | No | Yes | Yes |
| **Staff: Add, Update, Delete** | No | No | Yes |
