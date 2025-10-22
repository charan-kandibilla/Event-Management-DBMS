# Event Management System (DBMS + Tkinter)

A desktop-based event management application built using **MySQL** for data storage and **Tkinter** for the GUI.  
It manages events, venues, vendors, volunteers, performances, and attendees, with features for both **admin** and **general** users.

---

## How it works
- **Backend (MySQL):**
  - Normalized relational schema with foreign keys, constraints, triggers, and stored functions.
  - Tables for `events`, `headorg`, `vendors`, `volunteers`, `tasks`, `venue`, `performance`, `performer`, `attendees`, and junction tables.
  - Business rules enforced using **triggers** (e.g., performer limit, unique venue per event, non-negative vendor fee).
  - Stored function to calculate total vendor revenue per event.

- **Frontend (Tkinter):**
  - GUI windows for viewing, adding, updating, and deleting records.
  - Role-based access: **Admin login** for managing records, public interface for viewing schedules.
  - Dynamic table-like layouts for displaying database data with action buttons.

---

## Key data structures & concepts
- **Relational DBMS concepts:** primary/foreign keys, cascading deletes, composite keys, ENUM, UNIQUE constraints, triggers, stored functions.
- **GUI development:** Tkinter widgets (Labels, Buttons, Entry, Canvas, Scrollbar, Frames), dynamic layouts, separate windows for CRUD operations.
- **Backend-frontend interaction:** `mysql.connector` for executing SQL queries from Python.
- **Data validation & constraints:** implemented in both SQL triggers and Python checks.

---

## Features
- **Event Management:** Create, view, update, delete events with linked venue, vendors, volunteers, performances, and attendees.
- **Vendor Management:** Add, update, delete vendors; automatic revenue calculation per event.
- **Volunteer & Task Management:** Assign volunteers to heads and link tasks to them.
- **Venue Management:** Ensure one venue per event with uniqueness constraints.
- **Performance Scheduling:** Add performances with performer limits enforced by triggers.
- **Attendee Registration:** Capture attendee details, payment info, and event category.

---

## Build & run
**Requirements:**
- Python 3.x  
- MySQL Server  
- `mysql-connector-python` package

**Steps:**
1. Import the provided SQL script into MySQL to create the database and tables.
2. Update database connection details (`host`, `user`, `password`, `database`) in the Python script.
3. Install dependencies:
      pip install mysql-connector-python
4. Run the Python GUI:
      python app.py
---

## Limitations & Ideas to Extend

**Current:**
- GUI layout is functional but basic.
- No search/filter features for large datasets.
- Minimal form validation in the frontend.

**Possible Extensions:**
- Add attendee ticket generation.
- Export reports in PDF/Excel.
- Add date pickers for scheduling.
- Implement search and filter functionality.
- Improve UI with `ttk` themed widgets.

---

## What I Learnt
- Designing a multi-table relational database with constraints and relationships.
- Integrating a Python GUI with MySQL.
- Implementing business rules using triggers and stored functions.
- Building CRUD-based interfaces with Tkinter.
