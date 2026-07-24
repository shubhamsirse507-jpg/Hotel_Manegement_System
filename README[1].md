# Hotel Management System (HMS)

A **CLI-only** hotel management application built with Python and MySQL.

## Quick Start

```bash
# Install dependencies
pip install mysql-connector-python reportlab matplotlib

# Run the CLI
python main.py
```

## Project Structure

```
HMS_Project/
├── main.py               ← CLI entry point (role-based menus, payment + email receipt)
├── db.py                 ← Shared MySQL connection module
├── reports.py            ← Analytics charts (matplotlib → reports/)
├── README.md
│
├── cli/                  ← All CLI business-logic modules
│   ├── __init__.py
│   ├── authentication.py   — login(), returns role string
│   ├── rooms.py            — room catalog CRUD
│   ├── booking.py          — book / check-in / check-out
│   ├── billing.py          — bills, payments, PDF receipts
│   ├── service.py          — service request CRUD
│   ├── staff.py            — staff & housekeeping management
│   └── guest.py            — guest CRUD
│
├── tools/                ← Developer / diagnostic utilities
│   └── check_db.py         — inspect DB schema & users table
│
├── docs/                 ← Project documentation
│   ├── project_description.md
│   └── Flow.txt
│
├── legacy/               ← Archived superseded drafts (reference only — do not import)
│   ├── README.md
│   ├── auth.py
│   ├── Auth2.py
│   ├── bill.py
│   └── bill2.py
│
├── receipts/             ← Generated PDF payment receipts
└── reports/              ← Generated analytics charts (PNG)
```

## Roles & Default Passwords

| Role | Password |
|---|---|
| Admin | `admin123` |
| Manager | `manager123` |
| Receptionist | `reception123` |

## Role Access Map

| Feature | Receptionist | Manager | Admin |
|---|:---:|:---:|:---:|
| Room: View & Search | ✅ | ✅ | ✅ |
| Room: Add & Update | ❌ | ✅ | ✅ |
| Room: Delete | ❌ | ❌ | ✅ |
| Guest Management (full CRUD) | ✅ | ✅ | ✅ |
| Booking: Create, Modify, Cancel, Check-in/out | ✅ | ✅ | ✅ |
| Billing: Create, View, Search, Pay | ✅ | ✅ | ✅ |
| Billing: Update | ❌ | ✅ | ✅ |
| Billing: Delete | ❌ | ❌ | ✅ |
| Service Requests: Add, View, Update | ✅ | ✅ | ✅ |
| Service Requests: Delete | ❌ | ❌ | ✅ |
| Staff & Housekeeping: View, Assign | ❌ | ✅ | ✅ |
| Staff: Add, Update, Delete | ❌ | ❌ | ✅ |

## Email Receipts

Set environment variables before running (optional):

```bash
set HOTEL_SENDER_EMAIL=your@gmail.com
set HOTEL_APP_PASSWORD=your_gmail_app_password
```

## Developer Tools

```bash
# Check DB connection & inspect users table
python tools/check_db.py

# Generate analytics reports (room status, revenue, bookings by type)
python reports.py
```

See `docs/project_description.md` for full architecture details.
