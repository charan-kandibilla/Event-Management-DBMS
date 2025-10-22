import tkinter as tk
import mysql.connector
from tkinter import messagebox, Toplevel, Scrollbar, Frame, Entry, StringVar, Label

DB_HOST = "localhost"
DB_USER = "root"  # Replace with your MySQL username
DB_PASSWORD = "xyz"  # Replace with your MySQL password
DB_DATABASE = "EventManagement"

#1nf no composite, no multivalued attributes
#2nf, 1nf + non prime attributes should be dependent on primary key and not on parts of it
#3nf, 2nf+ no transitive dependency bw non primary attribute and primary key

#SHOW PROCEDURE STATUS WHERE Db = 'eventmanagement';
#SHOW Function STATUS WHERE Db = 'your_database_name';


# Function to connect to the database
def connect_db():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_DATABASE
    )


def show_login_fields():
    # Hide the initial buttons
    admin_login_btn.place_forget()
    register_btn.place_forget()
    event_schedule_btn.place_forget()
    
    # Display the head_id and login_cred (password) fields and the submit button
    lbl_head_id.place(x=50, y=50)
    head_id_entry.place(x=150, y=50, width=100)
    lbl_password.place(x=50, y=90)
    password_entry.place(x=150, y=90, width=100)
    submit_btn.place(x=150, y=130, width=80)

def admin_login():
    head_id = head_id_entry.get()
    login_cred = password_entry.get()
    logintodb(head_id, login_cred)

def logintodb(head_id, login_cred):
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",      # Replace with MySQL username
            password="xyz",  # Replace with MySQL password
            database="EventManagement"
        )
        cursor = db.cursor()
        
        if verify_admin(cursor, head_id, login_cred):
            messagebox.showinfo("Success", "Admin login successful!")
            display_events(cursor, head_id)
        else:
            messagebox.showerror("Error", "Invalid admin credentials.")
            
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        if db.is_connected():
            db.close()

def verify_admin(cursor, head_id, login_cred):
    verify_query = "SELECT * FROM headOrg WHERE head_id = %s AND login_cred = %s"
    cursor.execute(verify_query, (head_id, login_cred))
    return cursor.fetchone() is not None

def display_event_schedule():
    # Clear the main screen and open a new Toplevel window for the schedule
    schedule_window = tk.Toplevel(root)
    schedule_window.title("Event Schedule")
    schedule_window.geometry("400x300")
    
    # Header Label
    header_label = tk.Label(schedule_window, text="Select an Event to View Details", font=("Arial", 16, "bold"), fg="#3b5998")
    header_label.grid(row=0, column=0, columnspan=2, pady=20)

    # Query to fetch event names
    db = connect_db()
    cursor = db.cursor()
    event_query = "SELECT event_id, event_name FROM Events"
    cursor.execute(event_query)
    events = cursor.fetchall()
    db.close()
    
    # Create a button for each event in the schedule_window
    for idx, (event_id, event_name) in enumerate(events, start=1):
        event_btn = tk.Button(schedule_window, text=event_name, font=("Arial", 12), fg="white", bg="#4CAF50",
                              command=lambda eid=event_id: show_event_details(eid))
        event_btn.grid(row=idx, column=0, padx=10, pady=5, sticky="w")

    # Back Button in the schedule_window
    back_button = tk.Button(schedule_window, text="Back", font=("Arial", 12), fg="white", bg="#f44336", command=schedule_window.destroy)
    back_button.grid(row=idx + 1, column=0, padx=10, pady=20, sticky="w")

def show_event_details(event_id):
    # Create a new Toplevel window
    details_window = tk.Toplevel(root)
    details_window.title("Event Details")
    details_window.geometry("600x600")
    details_window.configure(bg="#f7f7f7")
    
    # Frame for content alignment
    content_frame = tk.Frame(details_window, bg="#f7f7f7")
    content_frame.pack(pady=15, padx=15, fill="both", expand=True)
    
    # Display headers in the new window with better styling
    headers = ["Event Name", "Event Date", "Venue Name", "Address"]
    for col, text in enumerate(headers):
        label = tk.Label(content_frame, text=text, font=("Arial", 12, "bold"), fg="#333", bg="#f7f7f7")
        label.grid(row=0, column=col, padx=10, pady=5, sticky="w")

    # Nested query to fetch event, venue, and performance details
    db = connect_db()
    cursor = db.cursor()
    details_query = """
        SELECT e.event_name, e.event_date, v.venue_name, v.address, 
       p.performance_name, p.start_time, p.end_time
        FROM Events e
        JOIN Venue v ON e.event_id = v.event_id
        LEFT JOIN (
            SELECT performance_name, start_time, end_time, event_id 
            FROM Performance
        ) AS p ON e.event_id = p.event_id
        WHERE e.event_id = %s;

    """
    cursor.execute(details_query, (event_id,))
    event_details = cursor.fetchall()
    
    # Display the main event and venue details
    if event_details:
        event_name, event_date, venue_name, address = event_details[0][:4]
        row_color = "#ffffff"
        
        # Display event and venue details in a single row
        detail_labels = [event_name, event_date, venue_name, address]
        for col, value in enumerate(detail_labels):
            label = tk.Label(content_frame, text=value, font=("Arial", 10), fg="#555", bg=row_color,
                             relief="solid", padx=10, pady=5, anchor="w")
            label.grid(row=1, column=col, padx=10, pady=5, sticky="w")

        # Add a section for Performance details
        performance_label = tk.Label(content_frame, text="Performances", font=("Arial", 12, "bold"), bg="#f7f7f7")
        performance_label.grid(row=3, column=0, columnspan=4, pady=(20, 10), sticky="w")
        
        # Headers for performance details
        performance_headers = ["Performance Name", "Start Time", "End Time"]
        for col, text in enumerate(performance_headers):
            label = tk.Label(content_frame, text=text, font=("Arial", 10, "bold"), fg="#333", bg="#f7f7f7")
            label.grid(row=4, column=col, padx=10, pady=5, sticky="w")
        
        # Display performance details from the nested query results
        for row_idx, detail in enumerate(event_details, start=5):
            _, _, _, _, performance_name, start_time, end_time = detail
            if performance_name:
                performance_values = [performance_name, start_time, end_time]
                for col, value in enumerate(performance_values):
                    row_color = "#ffffff" if row_idx % 2 == 0 else "#f9f9f9"  # Alternating row colors
                    label = tk.Label(content_frame, text=value, font=("Arial", 10), fg="#555", bg=row_color,
                                     relief="solid", padx=10, pady=5, anchor="w")
                    label.grid(row=row_idx, column=col, padx=10, pady=5, sticky="w")
            else:
                no_performance_label = tk.Label(content_frame, text="No performances found for this event.",
                                                font=("Arial", 10), fg="#D9534F", bg="#f7f7f7")
                no_performance_label.grid(row=5, column=0, columnspan=3, padx=10, pady=10)
                break
    else:
        no_details_label = tk.Label(content_frame, text="No details found for this event.",
                                    font=("Arial", 10), fg="#D9534F", bg="#f7f7f7")
        no_details_label.grid(row=1, column=0, columnspan=len(headers), padx=10, pady=10)
    
    db.close()
    
    # Separator line at the bottom for a clean finish
    separator = tk.Label(details_window, text="", bg="#CCCCCC")
    separator.pack(fill="x", padx=15, pady=(0, 15))
    
    # Close Button at the bottom
    close_btn = tk.Button(details_window, text="Close", command=details_window.destroy, 
                          bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), relief="solid")
    close_btn.pack(pady=10, padx=20, fill="x")

def display_events(cursor, head_id):
    # Clear the current screen
    clear_screen()

    # Display headers
    headers = ["Event ID", "Event Name", "Event Date"]
    for col, text in enumerate(headers):
        label = tk.Label(root, text=text, font=("Arial", 12, "bold"))
        label.grid(row=0, column=col, padx=10, pady=5)
    
    # Query to fetch events organized by the logged-in head_id
    event_query = "SELECT * FROM Events WHERE head_id = %s"
    cursor.execute(event_query, (head_id,))
    events = cursor.fetchall()
    
    # Display events in a table format
    for row, event in enumerate(events, start=1):
        for col, value in enumerate(event[:-1]):  # Exclude head_id for display
            label = tk.Label(root, text=value, font=("Arial", 10))
            label.grid(row=row, column=col, padx=10, pady=5)
        
        # Create a button for each event
        event_btn = tk.Button(root, text=f"Details for Event ID {event[0]}", command=lambda eid=event[0]: show_volunteer_window(eid))
        event_btn.grid(row=row, column=len(headers), padx=10, pady=5)

    # No events found message
    if not events:
        no_events_label = tk.Label(root, text="No events found for this head ID.", font=("Arial", 10))
        no_events_label.grid(row=1, column=0, columnspan=len(headers), padx=10, pady=10)



def show_volunteer_window(event_id):
    # Create a new window for volunteer details
    volunteer_window = Toplevel(root)
    volunteer_window.title("Event Details")
    volunteer_window.geometry("600x600")

    # Button to show volunteer details
    volunteer_button = tk.Button(volunteer_window, text="Show Volunteer Details", command=lambda eid=event_id: show_volunteer_details(volunteer_window, eid))
    volunteer_button.pack(pady=10)

    show_venue_button = tk.Button(volunteer_window, text="Show Venue Details", command=lambda eid=event_id: display_venue_details(volunteer_window, eid))
    show_venue_button.pack(pady=10)

    show_vendor_button = tk.Button(volunteer_window, text="Show Vendor Details", command=lambda eid=event_id: show_vendor_details(volunteer_window, eid))
    show_vendor_button.pack(pady=10)

    show_performance_button = tk.Button(volunteer_window, text="Show Performances", command=lambda: show_performance_window(event_id))
    show_performance_button.pack(pady=10)

    # Create a button to show attendee details and call the view_attendees function
    show_attendees_button = tk.Button(volunteer_window, text="Show Attendees", command=lambda: view_attendees(event_id))
    show_attendees_button.pack(pady=10)




def show_performance_window(event_id):
    # Create the window for showing performance details
    performance_window = tk.Toplevel()
    performance_window.title("Performance Details")

    # Now show the performance details for the specific event
    show_performance_details(performance_window, event_id)

def show_performance_details(performance_window, event_id):
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="xyz",
            database="EventManagement"
        )
        cursor = db.cursor()

        # Fetch performances for the specific event_id
        performance_query = """SELECT p.performance_name, p.no_of_performers, p.start_time, p.end_time
                               FROM performance p
                               WHERE p.event_id = %s;"""
        
        cursor.execute(performance_query, (event_id,))
        performances = cursor.fetchall()

        count_query = """SELECT COUNT(*) FROM performance p WHERE p.event_id = %s;"""
        cursor.execute(count_query, (event_id,))
        num_performances = cursor.fetchone()[0]  # Fetch the count result

        # Clear existing widgets in the performance window
        for widget in performance_window.winfo_children():
            widget.destroy()

        # Add header buttons
        performance_button = tk.Button(performance_window, text="Show Performance Details", command=lambda: show_performance_details(performance_window, event_id))
        performance_button.grid(row=0, column=0, padx=10, pady=10, columnspan=2, sticky="w")

        add_performance_button = tk.Button(performance_window, text="Add Performance", command=lambda: add_performance_window(event_id))
        add_performance_button.grid(row=0, column=2, padx=10, pady=10, columnspan=2, sticky="w")

        # Display header for performance details
        headers = ["Performance Name", "No. of Performers", "Start Time", "End Time", "Actions"]
        for idx, header in enumerate(headers):
            label = tk.Label(performance_window, text=header, font=("Arial", 12, "bold"))
            label.grid(row=1, column=idx, padx=10, pady=5)


        # Display each performance's details with update and delete buttons
        for row_idx, performance in enumerate(performances, start=2):  # Start from row 2 after headers
            performance_name, no_of_performers, start_time, end_time = performance

            # Display performance details in the table
            tk.Label(performance_window, text=performance_name).grid(row=row_idx, column=0, padx=10, pady=5)
            tk.Label(performance_window, text=str(no_of_performers)).grid(row=row_idx, column=1, padx=10, pady=5)
            tk.Label(performance_window, text=str(start_time)).grid(row=row_idx, column=2, padx=10, pady=5)
            tk.Label(performance_window, text=str(end_time)).grid(row=row_idx, column=3, padx=10, pady=5)

            # Update and Delete buttons for each performance
            update_button = tk.Button(performance_window, text="Update", command=lambda pname=performance_name: update_performance_window(pname))
            update_button.grid(row=row_idx, column=5, padx=5, pady=5)

            delete_button = tk.Button(performance_window, text="Delete", command=lambda pname=performance_name: delete_performance(pname, performance_window,event_id))
            delete_button.grid(row=row_idx, column=6, padx=5, pady=5)

            # View Performer Details button
            view_performer_button = tk.Button(performance_window, text="View Performer Details", command=lambda pname=performance_name: show_performer_details(pname, event_id))
            view_performer_button.grid(row=row_idx, column=7, padx=5, pady=5)

        def show_num_performances():
            messagebox.showinfo("Number of Performances", f"Total Performances: {num_performances}")

        # Add the button at the bottom of the window to show the number of performances
        show_count_button = tk.Button(performance_window, text="Show Number of Performances", command=show_num_performances)
        show_count_button.grid(row=len(performances) + 2, column=0, columnspan=8, padx=10, pady=10)

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        if db.is_connected():
            db.close()


def show_performer_details(performance_name, event_id):
    # Create a new window to display performers
    performer_window = Toplevel(root)
    performer_window.title(f"Performers for {performance_name}")
    performer_window.geometry("600x400")

    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="xyz",
            database="EventManagement"
        )
        cursor = db.cursor()

        # Fetch performers for the specific performance
        performer_query = """SELECT pr.performer_id, pr.performer_name, TIMESTAMPDIFF(YEAR, pr.dob, CURDATE()) AS age, pb.role 
                             FROM performer pr
                             JOIN performed_by pb ON pr.performer_id = pb.performer_id
                             WHERE pb.performance_name = %s;"""
        
        cursor.execute(performer_query, (performance_name,))
        performers = cursor.fetchall()

        # Clear existing widgets in the performer window
        for widget in performer_window.winfo_children():
            widget.destroy()

        # Header for performer details
        headers = ["Performer ID", "Name", "Age", "Role", "Actions"]
        for idx, header in enumerate(headers):
            label = tk.Label(performer_window, text=header, font=("Arial", 12, "bold"))
            label.grid(row=0, column=idx, padx=10, pady=5)

        # Display each performer's details with update and delete buttons
        for row_idx, performer in enumerate(performers, start=1):
            performer_id, performer_name, age, role = performer

            # Display performer details in the table
            tk.Label(performer_window, text=str(performer_id)).grid(row=row_idx, column=0, padx=10, pady=5)
            tk.Label(performer_window, text=performer_name).grid(row=row_idx, column=1, padx=10, pady=5)
            tk.Label(performer_window, text=str(age)).grid(row=row_idx, column=2, padx=10, pady=5)
            tk.Label(performer_window, text=role).grid(row=row_idx, column=3, padx=10, pady=5)

            # Update and Delete buttons for each performer
            update_button = tk.Button(performer_window, text="Update", command=lambda pid=performer_id: update_performer_window(pid))
            update_button.grid(row=row_idx, column=4, padx=5, pady=5)

            delete_button = tk.Button(performer_window, text="Delete", command=lambda pid=performer_id: delete_performer(pid, performer_window, performance_name, event_id))
            delete_button.grid(row=row_idx, column=5, padx=5, pady=5)

        # Button to add a new performer
        add_button = tk.Button(performer_window, text="Add Performer", command=lambda: add_performer_window(performance_name, event_id))
        add_button.grid(row=len(performers) + 1, column=0, columnspan=6, pady=10)

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        if db.is_connected():
            db.close()

def show_message(message):
    messagebox.showinfo("Error", message)

def add_performer_window(performance_name,event_id):
    # Create a new window for adding a performer
    add_window = Toplevel(root)
    add_window.title("Add Performer")
    add_window.geometry("400x300")

    # Input fields for new performer details
    tk.Label(add_window, text="Name:").pack()
    name_entry = tk.Entry(add_window)
    name_entry.pack()

    tk.Label(add_window, text="DOB (YYYY-MM-DD):").pack()
    dob_entry = tk.Entry(add_window)
    dob_entry.pack()

    tk.Label(add_window, text="Role:").pack()
    role_entry = tk.Entry(add_window)
    role_entry.pack()

    tk.Label(add_window, text="Phone no.:").pack()
    pn_entry = tk.Entry(add_window)
    pn_entry.pack()

    def add_performer_to_db():
        name = name_entry.get()
        dob = dob_entry.get()  # Assuming dob_entry is the entry widget for Date of Birth
        role = role_entry.get()
        pn = pn_entry.get()

        try:
            db = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_DATABASE
            )
            cursor = db.cursor()
            

            # Insert the new performer into the performer table
            insert_query = "INSERT INTO performer (performer_name, dob, phone_no, event_id) VALUES (%s, %s, %s, %s)"
            cursor.execute(insert_query, (name, dob, pn, event_id))  # Assuming dob is passed in YYYY-MM-DD format
            performer_id = cursor.lastrowid  # Get the ID of the newly inserted performer

            # Insert into performed_by table, including role and linking performer to performance
            link_query = "INSERT INTO performed_by (performer_id, role, performance_name) VALUES (%s, %s, %s)"
            cursor.execute(link_query, (performer_id, role, performance_name))

            db.commit()
            messagebox.showinfo("Success", "Performer added successfully.")
            add_window.destroy()  # Close the add performer window
            show_performer_details(performance_name, event_id)  # Refresh the performer list

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            if db.is_connected():
                db.close()

    # Button to add performer to the database
    add_button = tk.Button(add_window, text="Add Performer", command=add_performer_to_db)
    add_button.pack(pady=10)

def update_performer_window(performer_id):
    # Create a window to update performer details
    update_window = Toplevel(root)
    update_window.title("Update Performer")
    update_window.geometry("400x300")

    # Input fields for performer details to update
    tk.Label(update_window, text="Name:").pack()
    name_entry = tk.Entry(update_window)
    name_entry.pack()

    tk.Label(update_window, text="DOB:").pack()
    age_entry = tk.Entry(update_window)
    age_entry.pack()

    tk.Label(update_window, text="Role:").pack()
    role_entry = tk.Entry(update_window)
    role_entry.pack()

    def update_performer_in_db():
        name = name_entry.get()
        dob = age_entry.get()
        role = role_entry.get()

        try:
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="xyz",
                database="EventManagement"
            )
            cursor = db.cursor()

            update_performer_query = "UPDATE performer SET performer_name = %s, dob = %s WHERE performer_id = %s"
            cursor.execute(update_performer_query, (name, dob, performer_id))

            # Update the role in the performed_by table
            update_role_query = "UPDATE performed_by SET role = %s WHERE performer_id = %s"
            cursor.execute(update_role_query, (role, performer_id))

            db.commit()
            messagebox.showinfo("Success", "Performer updated successfully.")
            update_window.destroy()  # Close the update performer window

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            if db.is_connected():
                db.close()

    # Button to update performer in the database
    update_button = tk.Button(update_window, text="Update Performer", command=update_performer_in_db)
    update_button.pack(pady=10)

def delete_performer(performer_id, performer_window, performance_name, event_id):
    # Delete performer from the database
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="xyz",
            database="EventManagement"
        )
        cursor = db.cursor()

        # Delete performer from the performed_by table first
        delete_link_query = "DELETE FROM performed_by WHERE performer_id = %s"
        cursor.execute(delete_link_query, (performer_id,))

        # Delete performer from the performer table
        delete_performer_query = "DELETE FROM performer WHERE performer_id = %s"
        cursor.execute(delete_performer_query, (performer_id,))

        db.commit()
        messagebox.showinfo("Success", "Performer deleted successfully.")
        show_performer_details(performance_name, event_id)  # Refresh the performer list

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        if db.is_connected():
            db.close()


# Function to add a new performance
def add_performance_window(event_id):
    add_window = tk.Toplevel()
    add_window.title("Add Performance")

    def add_performance():
        performance_name = performance_name_entry.get()
        no_of_performers = no_of_performers_entry.get()
        start_time = start_time_entry.get()
        end_time = end_time_entry.get()

        if not performance_name or not no_of_performers or not start_time or not end_time:
            messagebox.showerror("Input Error", "Please fill all fields.")
            return

        try:
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="xyz",
                database="EventManagement"
            )
            cursor = db.cursor()

            add_query = """INSERT INTO performance (performance_name, no_of_performers, start_time, end_time, event_id)
                           VALUES (%s, %s, %s, %s, %s);"""
            
            cursor.execute(add_query, (performance_name, no_of_performers, start_time, end_time, event_id))
            db.commit()

            messagebox.showinfo("Success", "Performance added successfully.")
            add_window.destroy()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            if db.is_connected():
                db.close()

    # Create input fields and labels for new performance details
    tk.Label(add_window, text="Performance Name").pack(pady=5)
    performance_name_entry = tk.Entry(add_window)
    performance_name_entry.pack(pady=5)

    tk.Label(add_window, text="No. of Performers").pack(pady=5)
    no_of_performers_entry = tk.Entry(add_window)
    no_of_performers_entry.pack(pady=5)

    tk.Label(add_window, text="Start Time (HH:MM:SS)").pack(pady=5)
    start_time_entry = tk.Entry(add_window)
    start_time_entry.pack(pady=5)

    tk.Label(add_window, text="End Time (HH:MM:SS)").pack(pady=5)
    end_time_entry = tk.Entry(add_window)
    end_time_entry.pack(pady=5)

    # Submit button to add performance
    submit_button = tk.Button(add_window, text="Add Performance", command=add_performance)
    submit_button.pack(pady=10)

# Function to update performance (based on performance_name)
def update_performance_window(performance_name):
    update_window = tk.Toplevel()
    update_window.title("Update Performance")

    def update_performance():
        no_of_performers = no_of_performers_entry.get()
        start_time = start_time_entry.get()
        end_time = end_time_entry.get()

        if not no_of_performers or not start_time or not end_time:
            messagebox.showerror("Input Error", "Please fill all fields.")
            return

        try:
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="xyz",
                database="EventManagement"
            )
            cursor = db.cursor()

            update_query = """UPDATE performance
                              SET no_of_performers = %s, start_time = %s, end_time = %s
                              WHERE performance_name = %s;"""
            
            cursor.execute(update_query, (no_of_performers, start_time, end_time, performance_name))
            db.commit()

            messagebox.showinfo("Success", "Performance updated successfully.")
            update_window.destroy()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            if db.is_connected():
                db.close()

    # Create input fields and labels for updating performance
    tk.Label(update_window, text="No. of Performers").pack(pady=5)
    no_of_performers_entry = tk.Entry(update_window)
    no_of_performers_entry.pack(pady=5)

    tk.Label(update_window, text="Start Time (HH:MM:SS)").pack(pady=5)
    start_time_entry = tk.Entry(update_window)
    start_time_entry.pack(pady=5)

    tk.Label(update_window, text="End Time (HH:MM:SS)").pack(pady=5)
    end_time_entry = tk.Entry(update_window)
    end_time_entry.pack(pady=5)

    # Submit button to update performance
    submit_button = tk.Button(update_window, text="Update Performance", command=update_performance)
    submit_button.pack(pady=10)

# Function to delete a performance (based on performance_name)
def delete_performance(performance_name, performance_window,event_id):
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="xyz",
            database="EventManagement"
        )
        cursor = db.cursor()

        delete_query = """DELETE FROM performance WHERE performance_name = %s;"""
        cursor.execute(delete_query, (performance_name,))
        db.commit()

        messagebox.showinfo("Success", "Performance deleted successfully.")
        show_performance_details(performance_window, event_id)  # Refresh the performance list

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        if db.is_connected():
            db.close()

#attendees
def verify_attendee(cursor, reg_id, email):
    verify_query = "SELECT * FROM attendees WHERE reg_id = %s AND email = %s"
    cursor.execute(verify_query, (reg_id, email))
    return cursor.fetchone() is not None

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="xyz",
    database="eventmanagement"
)
cursor = conn.cursor()

# Function to add attendee
def add_attendee():
    def submit_attendee():
        # Get attendee details from entry fields
        name = entry_name.get()
        age = entry_age.get()
        amount = entry_amount.get()
        email = entry_email.get()
        category = var_category.get()
        event_name = var_event.get()  # Get the selected event name from option menu
        
        # Retrieve the event_id based on the selected event name
        cursor.execute("SELECT event_id FROM events WHERE event_name = %s", (event_name,))
        event_id = cursor.fetchone()[0]
        
        try:
            # Call the stored procedure to insert the attendee
            cursor.callproc('RegisterAttendeeWithUniqueEmail', 
                             (name, age, amount, email, category, event_id))
            
            # Commit the transaction
            conn.commit()
            
            # Fetch the generated reg_id for the newly inserted attendee (if no error)
            reg_id = cursor.lastrowid
            messagebox.showinfo("Registration Successful", f"Registration Successful")
            add_window.destroy()

        except mysql.connector.Error as err:
            # Handle the error, such as duplicate email or any other database error
            messagebox.showerror("Registration Error", f"Error: {err}")

    def update_amount(*args):
        # Update the amount based on the selected category
        if var_category.get() == "general":
            entry_amount.delete(0, tk.END)
            entry_amount.insert(0, "350")
            print("Amount Paid set to: 350")
        elif var_category.get() == "vip":
            entry_amount.delete(0, tk.END)
            entry_amount.insert(0, "500")
            print("Amount Paid set to: 500")

    # Create a new window for adding attendee
    add_window = tk.Toplevel()
    add_window.title("Register Attendee")
    add_window.geometry("600x300")

    # Entry fields for attendee details
    tk.Label(add_window, text="Name").grid(row=0, column=0)
    entry_name = tk.Entry(add_window)
    entry_name.grid(row=0, column=1)

    tk.Label(add_window, text="Age").grid(row=1, column=0)
    entry_age = tk.Entry(add_window)
    entry_age.grid(row=1, column=1)

    tk.Label(add_window, text="Email").grid(row=3, column=0)
    entry_email = tk.Entry(add_window)
    entry_email.grid(row=3, column=1)

    tk.Label(add_window, text="Category").grid(row=4, column=0)
    var_category = tk.StringVar(value="general")
    tk.OptionMenu(add_window, var_category, "general", "vip").grid(row=4, column=1)

    tk.Label(add_window, text="Amount Paid").grid(row=2, column=0)
    entry_amount = tk.Entry(add_window)
    entry_amount.grid(row=2, column=1)

    update_amount()
    # Set up trace to call update_amount whenever var_category changes
    var_category.trace("w", update_amount)

    # Retrieve events from the events table
    cursor.execute("SELECT event_name FROM events")
    events = [event[0] for event in cursor.fetchall()]  # List of event names

    # Event dropdown
    tk.Label(add_window, text="Event").grid(row=5, column=0)
    var_event = tk.StringVar(value=events[0])  # Default to the first event
    tk.OptionMenu(add_window, var_event, *events).grid(row=5, column=1)

    tk.Button(add_window, text="Submit", command=submit_attendee).grid(row=6, column=0, columnspan=2)

# Function to update or delete attendee
def update_delete_attendee():
    def verify_and_proceed():
        reg_id = entry_reg_id.get()
        email = entry_email.get()
        
        if verify_attendee(cursor, reg_id, email):
            action = var_action.get()
            if action == "update":
                open_update_window(reg_id)
            elif action == "delete":
                delete_attendee(reg_id)
                messagebox.showinfo("Deleted", f"Registration ID {reg_id} has been deleted.")
            update_delete_window.destroy()
        else:
            messagebox.showerror("Error", "Invalid Registration ID or Email")

    # Open a new window for update/delete operations
    update_delete_window = tk.Toplevel()
    update_delete_window.title("Update/Delete Registration")
    update_delete_window.geometry("500x300")


    tk.Label(update_delete_window, text="Registration ID").grid(row=0, column=0)
    entry_reg_id = tk.Entry(update_delete_window)
    entry_reg_id.grid(row=0, column=1)

    tk.Label(update_delete_window, text="Email").grid(row=1, column=0)
    entry_email = tk.Entry(update_delete_window)
    entry_email.grid(row=1, column=1)

    tk.Label(update_delete_window, text="Action").grid(row=2, column=0)
    var_action = tk.StringVar(value="update")
    tk.Radiobutton(update_delete_window, text="Update", variable=var_action, value="update").grid(row=2, column=1)
    tk.Radiobutton(update_delete_window, text="Delete", variable=var_action, value="delete").grid(row=2, column=2)

    tk.Button(update_delete_window, text="Proceed", command=verify_and_proceed).grid(row=3, column=0, columnspan=3)

# Function to verify attendee credentials
def verify_attendee(cursor, reg_id, email):
    verify_query = "SELECT * FROM attendees WHERE reg_id = %s AND email = %s"
    cursor.execute(verify_query, (reg_id, email))
    return cursor.fetchone() is not None

# Function to open update window after verification
def open_update_window(reg_id):
    def submit_update():
        new_name = entry_name.get()
        new_age = entry_age.get()
        new_amount = entry_amount.get()
        new_email = entry_email.get()
        new_category = var_category.get()
        
        # Update the attendee details in the database
        update_query = """
            UPDATE attendees
            SET att_name = %s, att_age = %s, amount_paid = %s, email = %s, category = %s
            WHERE reg_id = %s
        """
        cursor.execute(update_query, (new_name, new_age, new_amount, new_email, new_category, reg_id))
        conn.commit()
        messagebox.showinfo("Update Successful", f"Registration ID {reg_id} has been updated.")
        update_window.destroy()

    # Create a new window for updating attendee information
    update_window = tk.Toplevel()
    update_window.title("Update Attendee")
    update_window.geometry("500x300")

    tk.Label(update_window, text="Name").grid(row=0, column=0)
    entry_name = tk.Entry(update_window)
    entry_name.grid(row=0, column=1)

    tk.Label(update_window, text="Age").grid(row=1, column=0)
    entry_age = tk.Entry(update_window)
    entry_age.grid(row=1, column=1)

    tk.Label(update_window, text="Amount Paid").grid(row=2, column=0)
    entry_amount = tk.Entry(update_window)
    entry_amount.grid(row=2, column=1)

    tk.Label(update_window, text="Email").grid(row=3, column=0)
    entry_email = tk.Entry(update_window)
    entry_email.grid(row=3, column=1)

    tk.Label(update_window, text="Category").grid(row=4, column=0)
    var_category = tk.StringVar(value="general")
    tk.OptionMenu(update_window, var_category, "general", "vip").grid(row=4, column=1)

    tk.Button(update_window, text="Submit", command=submit_update).grid(row=5, column=0, columnspan=2)

# Function to delete attendee
def delete_attendee(reg_id):
    delete_query = "DELETE FROM attendees WHERE reg_id = %s"
    cursor.execute(delete_query, (reg_id,))
    conn.commit()

# Main registration page
def register_page():
    register_window = tk.Toplevel()
    register_window.title("Attendee Registration")
    register_window.geometry("600x300")

    # Register button to open add attendee form
    tk.Button(register_window, text="Register", command=add_attendee, width=20, height=2).pack(pady=10)

    # Update/Delete Registration button
    tk.Button(register_window, text="Update/Delete Registration", command=update_delete_attendee, width=20, height=2).pack(pady=10)


def view_attendees(event_id):
    # Create a new window to display attendee details
    view_window = tk.Toplevel()
    view_window.title("View Attendees")
    view_window.geometry("700x400")

    # Define column headers for the attendee details
    headers = ["Reg ID", "Name", "Age", "Amount Paid", "Email", "Reg Date", "Category", "Event Name"]
    for col, header in enumerate(headers):
        tk.Label(view_window, text=header, font=('Arial', 10, 'bold')).grid(row=0, column=col, padx=5, pady=5)

    # Query to fetch attendee details along with the event name
    query = """
        SELECT a.reg_id, a.att_name, a.att_age, a.amount_paid, a.email, a.reg_date, a.category, e.event_name
        FROM attendees a
        LEFT JOIN events e ON a.event_id = e.event_id
        WHERE a.event_id = %s
    """
    cursor.execute(query,(event_id,))
    attendees = cursor.fetchall()

    # Display each attendee's details in a new row
    for row_idx, attendee in enumerate(attendees, start=1):
        for col_idx, value in enumerate(attendee):
            tk.Label(view_window, text=str(value)).grid(row=row_idx, column=col_idx, padx=5, pady=5)


    # Fetch the summary using the MySQL function 'get_attendee_summary'
    cursor.execute("SELECT get_attendee_summary1(%s)", (event_id,))
    summary = cursor.fetchone()[0]  # Fetch the summary string from the result

    tk.Label(view_window, text="Summary: " + summary, font=('Arial', 12, 'bold')).grid(row=len(attendees) + 1, column=0, columnspan=len(headers), pady=10)

    # Button to close the window
    tk.Button(view_window, text="Close", command=view_window.destroy).grid(row=len(attendees) + 2, column=0, columnspan=len(headers), pady=10)



def show_vendor_window(head_id, event_id):
    # Create a new window for vendor details
    vendor_window = Toplevel(root)
    vendor_window.title("Vendor Details")
    vendor_window.geometry("600x600")

    # Button to show vendor details
    vendor_button = tk.Button(vendor_window, text="Show Vendor Details", command=lambda eid=event_id: show_vendor_details(vendor_window, eid))
    vendor_button.pack(pady=10)

    # Button to add a vendor
    add_vendor_button = tk.Button(vendor_window, text="Add Vendor", command=lambda eid=event_id: add_vendor_window(eid))
    add_vendor_button.pack(pady=10)


def show_vendor_details(vendor_window, event_id):
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="xyz",
            database="EventManagement"
        )
        cursor = db.cursor()

        # Drop and create the SQL function for aggregate vendor fee specific to an event_id
        cursor.execute("DROP FUNCTION IF EXISTS total_vendor_revenue")
        
        create_function_query = """
        CREATE FUNCTION total_vendor_revenue(event_id INT) 
        RETURNS DECIMAL(10, 2)
        DETERMINISTIC
        BEGIN
            DECLARE total_revenue DECIMAL(10, 2);
            SELECT IFNULL(SUM(vendor_fee), 0) INTO total_revenue
            FROM vendors
            WHERE vendors.event_id = event_id;
            RETURN total_revenue;
        END
        """
        cursor.execute(create_function_query)

        # Fetch vendors based on the event_id
        vendor_query = """SELECT v.vendor_id, v.vendor_name, v.contact_details, v.services_provided, v.vendor_fee
                          FROM vendors v
                          WHERE v.event_id = %s;"""
        cursor.execute(vendor_query, (event_id,))
        vendors = cursor.fetchall()

        # If no vendors are found for this event_id
        if not vendors:
            messagebox.showinfo("No Vendors", "No vendors found for this event.")
            return

        # Clear the vendor_window if there are existing vendor details
        for widget in vendor_window.winfo_children():
            widget.destroy()

        # Display 'Show Vendor Details' and 'Add Vendor' buttons at the top
        vendor_button = tk.Button(vendor_window, text="Show Vendor Details", command=lambda eid=event_id: show_vendor_details(vendor_window, eid))
        vendor_button.grid(row=0, column=0, padx=10, pady=10, columnspan=2, sticky="w")

        add_vendor_button = tk.Button(vendor_window, text="Add Vendor", command=lambda eid=event_id: add_vendor_window(eid))
        add_vendor_button.grid(row=0, column=2, padx=10, pady=10, columnspan=2, sticky="w")

        # Display header for vendor details
        headers = ["Vendor ID", "Name", "Contact", "Service", "Fee", "Actions"]
        for idx, header in enumerate(headers):
            label = tk.Label(vendor_window, text=header, font=("Arial", 12, "bold"))
            label.grid(row=1, column=idx, padx=10, pady=5)

        # Display each vendor's details with update and delete buttons
        for row_idx, vendor in enumerate(vendors, start=2):  # Start from row 2 after headers
            vendor_id, vendor_name, contact, services, fee = vendor
            
            # Place each detail in a row with a Label widget
            tk.Label(vendor_window, text=vendor_id).grid(row=row_idx, column=0, padx=10, pady=5)
            tk.Label(vendor_window, text=vendor_name).grid(row=row_idx, column=1, padx=10, pady=5)
            tk.Label(vendor_window, text=contact).grid(row=row_idx, column=2, padx=10, pady=5)
            tk.Label(vendor_window, text=services).grid(row=row_idx, column=3, padx=10, pady=5)
            tk.Label(vendor_window, text=str(fee)).grid(row=row_idx, column=4, padx=10, pady=5)

            # Update and Delete buttons for each vendor
            update_button = tk.Button(vendor_window, text="Update", command=lambda vid=vendor_id: update_vendor_window(vid))
            update_button.grid(row=row_idx, column=5, padx=5, pady=5)

            delete_button = tk.Button(vendor_window, text="Delete", command=lambda vid=vendor_id: delete_vendor(vid, vendor_window))
            delete_button.grid(row=row_idx, column=6, padx=5, pady=5)

        # Fetch total vendor revenue for the specific event_id using the function total_vendor_revenue
        revenue_query = "SELECT total_vendor_revenue(%s)"
        cursor.execute(revenue_query, (event_id,))
        
        total_revenue = cursor.fetchone()[0]  # Get the revenue value

        # Display the total vendor revenue below the table
        total_revenue_label = tk.Label(vendor_window, text=f"Total Vendor Revenue for Event {event_id}: Rupees{total_revenue:.2f}", font=("Arial", 12, "bold"))
        total_revenue_label.grid(row=row_idx + 1, column=0, columnspan=6, pady=10)

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        if db.is_connected():
            db.close()


def add_vendor_window(event_id):
    add_window = Toplevel()
    add_window.title("Add Vendor")
    add_window.geometry("500x500")

    # Define variables for entry
    name_var = StringVar()
    contact_var = StringVar()
    services_var = StringVar()
    fee_var = StringVar()

    # Create labels and entry fields for vendor details
    tk.Label(add_window, text="Vendor Name:").pack(pady=5)
    name_entry = tk.Entry(add_window, textvariable=name_var)
    name_entry.pack(pady=5)

    tk.Label(add_window, text="Contact Number:").pack(pady=5)
    contact_entry = tk.Entry(add_window, textvariable=contact_var)
    contact_entry.pack(pady=5)

    tk.Label(add_window, text="Services Provided:").pack(pady=5)
    services_entry = tk.Entry(add_window, textvariable=services_var)
    services_entry.pack(pady=5)

    tk.Label(add_window, text="Vendor Fee:").pack(pady=5)
    fee_entry = tk.Entry(add_window, textvariable=fee_var)
    fee_entry.pack(pady=5)

    # Create labels and entry fields for head_id and event_id
    head_id = 1  # You can replace this with the actual head_id retrieval logic
    tk.Label(add_window, text="Head ID:").pack(pady=5)
    head_id_entry = tk.Entry(add_window)
    head_id_entry.insert(0, str(head_id))  # Set the default value to head_id
    head_id_entry.config(state='readonly')  # Make it read-only
    head_id_entry.pack(pady=5)

    tk.Label(add_window, text="Event ID:").pack(pady=5)
    event_id_entry = tk.Entry(add_window)
    event_id_entry.insert(0, str(event_id))  # Set the default value to event_id
    event_id_entry.config(state='readonly')  # Make it read-only
    event_id_entry.pack(pady=5)

    # Submit button for adding vendor
    submit_add_btn = tk.Button(
        add_window, 
        text="Add Vendor", 
        command=lambda: add_vendor(head_id, event_id, name_var.get(), contact_var.get(), services_var.get(), fee_var.get(), add_window)
    )
    submit_add_btn.pack(pady=20)



def add_vendor(head_id, event_id, name, contact, services, fee, window):
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="xyz",  # Change to your actual password
            database="EventManagement"
        )
        cursor = db.cursor()

        # Insert vendor details along with the head_id and event_id
        insert_query = """
        INSERT INTO vendors (vendor_name, contact_details, services_provided, vendor_fee, head_id, event_id)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (name, contact, services, fee, head_id, event_id))  # Add event_id here

        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS before_insert_vendor
            BEFORE INSERT ON vendors
            FOR EACH ROW
            BEGIN
                IF NEW.vendor_fee < 0 THEN
                    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Vendor fee cannot be negative';
                END IF;
            END;
        """)

    
        db.commit()

        messagebox.showinfo("Success", "Vendor added successfully!")
        window.destroy()  # Close the add vendor window

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        if db.is_connected():
            db.close()


def update_vendor_window(vendor_id):
    update_window = Toplevel(root)
    update_window.title("Update Vendor")
    update_window.geometry("300x400")

    # Define variables for entry
    name_var = StringVar()
    contact_var = StringVar()
    services_var = StringVar()
    fee_var = StringVar()
    event_id_var = StringVar()  # Variable to hold the event_id

    # Fetch current vendor details
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="xyz",
            database="EventManagement"
        )
        cursor = db.cursor()

        # Use correct column names: contact_details instead of contact_number
        select_query = "SELECT vendor_name, contact_details, services_provided, vendor_fee, event_id FROM vendors WHERE vendor_id = %s"
        cursor.execute(select_query, (vendor_id,))
        vendor = cursor.fetchone()

        # Set values in the entry fields if vendor data is available
        if vendor:
            name_var.set(vendor[0])
            contact_var.set(vendor[1])
            services_var.set(vendor[2])
            fee_var.set(vendor[3])
            event_id_var.set(vendor[4])  # Set the event_id for later use

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        if db.is_connected():
            db.close()

    # Create labels and entry fields
    Label(update_window, text="Vendor Name:").pack(pady=5)
    name_entry = Entry(update_window, textvariable=name_var)
    name_entry.pack(pady=5)

    Label(update_window, text="Contact Number:").pack(pady=5)
    contact_entry = Entry(update_window, textvariable=contact_var)
    contact_entry.pack(pady=5)

    Label(update_window, text="Services Provided:").pack(pady=5)
    services_entry = Entry(update_window, textvariable=services_var)
    services_entry.pack(pady=5)

    Label(update_window, text="Vendor Fee:").pack(pady=5)
    fee_entry = Entry(update_window, textvariable=fee_var)
    fee_entry.pack(pady=5)

    # Submit button for updating vendor
    submit_update_btn = tk.Button(
        update_window, 
        text="Update Vendor", 
        command=lambda: update_vendor(
            vendor_id, 
            name_var.get(), 
            contact_var.get(), 
            services_var.get(), 
            fee_var.get(), 
            event_id_var.get(),  # Pass the event_id
            update_window
        )
    )
    submit_update_btn.pack(pady=20)


def update_vendor(vendor_id, name, contact, services, fee, event_id, window):
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="xyz",
            database="EventManagement"
        )
        cursor = db.cursor()

        # Update vendor details with correct column name (contact_details)
        update_query = """
        UPDATE vendors 
        SET vendor_name = %s, contact_details = %s, services_provided = %s, vendor_fee = %s, event_id = %s 
        WHERE vendor_id = %s
        """
        cursor.execute(update_query, (name, contact, services, fee, event_id, vendor_id))

        
        db.commit()

        messagebox.showinfo("Success", "Vendor updated successfully!")
        window.destroy()  # Close the update vendor window

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        if db.is_connected():
            db.close()


def delete_vendor(vendor_id, vendor_window):
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="xyz",
            database="EventManagement"
        )
        cursor = db.cursor()

        # SQL query to delete the vendor based on vendor_id
        delete_query = "DELETE FROM vendors WHERE vendor_id = %s"
        cursor.execute(delete_query, (vendor_id,))

        # Commit the changes
        db.commit()

        # Refresh the vendor details after deletion
        messagebox.showinfo("Vendor Deleted", "Vendor has been deleted successfully.")
        show_vendor_details(vendor_window, event_id)  # Refresh the vendor details for the same event

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        if db.is_connected():
            db.close()

def add_volunteer_window(event_id):
    add_window = Toplevel(root)
    add_window.title("Add Volunteer")
    add_window.geometry("300x500")  # Adjust height to accommodate tasks

    # Define variables for entry
    name_var = StringVar()
    age_var = StringVar()
    gender_var = StringVar()
    phone_var = StringVar()
    head_var = StringVar()
    task_var = StringVar()  # New variable for task

    # Create labels and entry fields for volunteer information
    Label(add_window, text="Name:").pack(pady=5)
    name_entry = Entry(add_window, textvariable=name_var)
    name_entry.pack(pady=5)

    Label(add_window, text="Age:").pack(pady=5)
    age_entry = Entry(add_window, textvariable=age_var)
    age_entry.pack(pady=5)

    Label(add_window, text="Gender:").pack(pady=5)
    gender_entry = Entry(add_window, textvariable=gender_var)
    gender_entry.pack(pady=5)

    Label(add_window, text="Phone:").pack(pady=5)
    phone_entry = Entry(add_window, textvariable=phone_var)
    phone_entry.pack(pady=5)

    Label(add_window, text="Head ID:").pack(pady=5)
    head_entry = Entry(add_window, textvariable=head_var)
    head_entry.pack(pady=5)

    Label(add_window, text="Task:").pack(pady=5)  # New label for task
    task_entry = Entry(add_window, textvariable=task_var)  # New entry for task
    task_entry.pack(pady=5)

    # Submit button for adding volunteer
    submit_add_btn = tk.Button(add_window, text="Add Volunteer", command=lambda: add_volunteer(event_id, name_var.get(), age_var.get(), gender_var.get(), phone_var.get(), head_var.get(), task_var.get(), add_window))
    submit_add_btn.pack(pady=20)


def add_volunteer(event_id, name, age, gender, phone, head_id, task, window):
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="xyz",
            database="EventManagement"
        )
        cursor = db.cursor()

        # Insert volunteer
        insert_query = "INSERT INTO volunteers (vol_name, vol_age, vol_gender, phone_number, event_id, head_id) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (name, age, gender, phone, event_id, head_id))
        volunteer_id = cursor.lastrowid  # Get the ID of the newly added volunteer

        # Insert associated task if provided
        if task:
            task_query = "INSERT INTO tasks (task, volunteer_id, head_id) VALUES (%s, %s, %s)"
            cursor.execute(task_query, (task, volunteer_id, head_id))

        db.commit()
        messagebox.showinfo("Success", "Volunteer and task added successfully!")
        window.destroy()

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        if db.is_connected():
            db.close()


def delete_volunteer(volunteer_id, voluntee_window):
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",      # Replace with MySQL username
            password="xyz",  # Replace with MySQL password
            database="EventManagement"
        )
        cursor = db.cursor()

        # Correct the delete query to match the column name
        delete_query = "DELETE FROM volunteers WHERE volunteer_id = %s"
        cursor.execute(delete_query, (volunteer_id,))
        db.commit()

        messagebox.showinfo("Success", "Volunteer deleted successfully!")
        show_volunteer_details(voluntee_window, voluntee_window.winfo_children()[0].event_id)  # Refresh the volunteer details

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        if db.is_connected():
            db.close()


def show_volunteer_details(voluntee_window, event_id):
    voluntee_window = Toplevel(root)
    voluntee_window.title("Volunteer Details")
    voluntee_window.geometry("600x600")
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",      # Replace with MySQL username
            password="xyz",  # Replace with MySQL password
            database="EventManagement"
        )
        cursor = db.cursor()

        # Query to fetch volunteers with their assigned tasks
        # Query to fetch volunteers with their assigned tasks
        # Query to fetch volunteers with their assigned tasks based on head_id and volunteer_id
        volunteer_query = """
        SELECT v.volunteer_id, v.vol_name, v.vol_age, v.vol_gender, v.phone_number, 
        IFNULL(t.task, 'No Task') AS task
        FROM volunteers v
        LEFT JOIN tasks t ON v.volunteer_id = t.volunteer_id AND v.head_id = t.head_id
        WHERE v.event_id = %s
        """


        cursor.execute(volunteer_query, (event_id,))
        volunteers = cursor.fetchall()

        # Clear the window if there's existing volunteer details
        for widget in voluntee_window.winfo_children():
            widget.destroy()

        # Add the button again after clearing
        volunteer_button = tk.Button(voluntee_window, text="Show Volunteer Details", command=lambda eid=event_id: show_volunteer_details(voluntee_window, eid))
        volunteer_button.pack(pady=10)

        # Button to add a volunteer
        add_volunteer_button = tk.Button(voluntee_window, text="Add Volunteer", command=lambda eid=event_id: add_volunteer_window(eid))
        add_volunteer_button.pack(pady=10)

        # Create a frame for the table
        frame = Frame(voluntee_window)
        frame.pack(pady=10, fill='both', expand=True)

        # Create a scrollbar
        scrollbar = Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create a canvas for the volunteer details
        canvas = tk.Canvas(frame, yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=canvas.yview)

        # Create a new frame to hold the volunteer table
        table_frame = Frame(canvas)
        canvas.create_window((0, 0), window=table_frame, anchor="nw")

        # Prepare the volunteer details
        if volunteers:
            # Display headers for volunteer table
            headers = ["ID", "Name", "Age", "Gender", "Phone", "Task", "Actions"]
            for col, text in enumerate(headers):
                tk.Label(table_frame, text=text, font=("Arial", 10, "bold")).grid(row=0, column=col, padx=5, pady=5)

            # Display volunteer details in table format
            for row, volunteer in enumerate(volunteers, start=1):
                for col, value in enumerate(volunteer[:-1]):  # Exclude the last column for task display
                    label = tk.Label(table_frame, text=value, font=("Arial", 10))
                    label.grid(row=row, column=col, padx=5, pady=5)

                # Display task
                task_label = tk.Label(table_frame, text=volunteer[-1] if volunteer[-1] else "No Task", font=("Arial", 10))
                task_label.grid(row=row, column=5, padx=5, pady=5)

                # Create update button for each volunteer
                update_button = tk.Button(table_frame, text="Update", command=lambda vid=volunteer[0]: update_volunteer_window(vid, voluntee_window))
                update_button.grid(row=row, column=6, padx=5, pady=5)

                # Create delete button for each volunteer
                delete_button = tk.Button(table_frame, text="Delete", command=lambda vid=volunteer[0]: delete_volunteer(vid, voluntee_window))
                delete_button.grid(row=row, column=7, padx=5, pady=5)
        else:
            # Message if no volunteers found
            tk.Label(table_frame, text="No volunteers found for this event.", font=("Arial", 10)).grid(row=1, column=0, columnspan=7, padx=5, pady=5)

        # Adjust the scrollregion of the canvas
        table_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        if db.is_connected():
            db.close()

def update_volunteer_window(volunteer_id, voluntee_window):
    update_window = Toplevel(voluntee_window)
    update_window.title("Update Volunteer")
    update_window.geometry("300x500")  # Adjust height to accommodate tasks

    # Define variables for entry
    name_var = StringVar()
    age_var = StringVar()
    gender_var = StringVar()
    phone_var = StringVar()
    task_var = StringVar()  # New variable for task

    # Fetch current volunteer details
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="xyz",
            database="EventManagement"
        )
        cursor = db.cursor()

        cursor.execute("SELECT vol_name, vol_age, vol_gender, phone_number FROM volunteers WHERE volunteer_id = %s", (volunteer_id,))
        volunteer = cursor.fetchone()

        if volunteer:
            name_var.set(volunteer[0])
            age_var.set(volunteer[1])
            gender_var.set(volunteer[2])
            phone_var.set(volunteer[3])
            
            # Fetch the task associated with this volunteer
            cursor.execute("SELECT task FROM tasks WHERE volunteer_id = %s", (volunteer_id,))
            task = cursor.fetchone()
            task_var.set(task[0] if task else "")  # Set task if exists

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        if db.is_connected():
            db.close()

    # Create labels and entry fields for volunteer information
    Label(update_window, text="Name:").pack(pady=5)
    name_entry = Entry(update_window, textvariable=name_var)
    name_entry.pack(pady=5)

    Label(update_window, text="Age:").pack(pady=5)
    age_entry = Entry(update_window, textvariable=age_var)
    age_entry.pack(pady=5)

    Label(update_window, text="Gender:").pack(pady=5)
    gender_entry = Entry(update_window, textvariable=gender_var)
    gender_entry.pack(pady=5)

    Label(update_window, text="Phone:").pack(pady=5)
    phone_entry = Entry(update_window, textvariable=phone_var)
    phone_entry.pack(pady=5)

    Label(update_window, text="Task:").pack(pady=5)  # New label for task
    task_entry = Entry(update_window, textvariable=task_var)  # New entry for task
    task_entry.pack(pady=5)

    # Submit button for updating volunteer
    submit_update_btn = tk.Button(update_window, text="Update Volunteer", command=lambda: update_volunteer(volunteer_id, name_var.get(), age_var.get(), gender_var.get(), phone_var.get(), task_var.get(), update_window))
    submit_update_btn.pack(pady=20)


def update_volunteer(volunteer_id, name, age, gender, phone, task, window):
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="xyz",
            database="EventManagement"
        )
        cursor = db.cursor()

        # Update the volunteer information
        update_query = """
        UPDATE volunteers 
        SET vol_name = %s, vol_age = %s, vol_gender = %s, phone_number = %s 
        WHERE volunteer_id = %s
        """
        cursor.execute(update_query, (name, age, gender, phone, volunteer_id))

        # Update the associated task
        if task:
            task_query = "UPDATE tasks SET task = %s WHERE volunteer_id = %s"
            cursor.execute(task_query, (task, volunteer_id))
        else:
            # Optionally handle case where task is cleared (you could delete the task instead)
            delete_task_query = "DELETE FROM tasks WHERE volunteer_id = %s"
            cursor.execute(delete_task_query, (volunteer_id,))

        db.commit()
        messagebox.showinfo("Success", "Volunteer and task updated successfully!")
        window.destroy()  # Close the update window

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        if db.is_connected():
            db.close()


def display_venue_details(venue_window, event_id):
    venue_window = Toplevel(root)
    venue_window.title("Venue Details")
    venue_window.geometry("600x600")

    try:
        db = connect_db()
        cursor = db.cursor()
        venue_query = """
        SELECT v.venue_id, v.venue_name, v.address, v.capacity, e.event_date, e.event_name
        FROM venue v
        JOIN events e ON v.event_id = e.event_id
        WHERE v.event_id = %s
        """
        cursor.execute(venue_query, (event_id,))
        venues = cursor.fetchall()

        venue_button = tk.Button(venue_window, text="Show Venue Details", command=lambda eid=event_id: display_venue_details(venue_window, eid))
        venue_button.pack(pady=10)

        # Button to add a volunteer
        add_venue_button = tk.Button(venue_window, text="Add Venue", command=lambda eid=event_id: add_venue_window(eid))
        add_venue_button.pack(pady=10)


        frame = Frame(venue_window)
        frame.pack(pady=10, fill='both', expand=True)

        scrollbar = Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        canvas = tk.Canvas(frame, yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=canvas.yview)

        table_frame = Frame(canvas)
        canvas.create_window((0, 0), window=table_frame, anchor="nw")

        if venues:
           headers = ["Venue ID", "Venue Name", "Address", "Capacity", "Event Date", "Event name", "Actions"]
           for col, text in enumerate(headers):
               tk.Label(table_frame, text=text, font=("Arial", 10, "bold")).grid(row=0, column=col, padx=5, pady=5)

           for row, venue in enumerate(venues, start=1):
        # Assuming venue returns a tuple: (venue_id, venue_name, address, capacity, event_id, event_date)
               tk.Label(table_frame, text=venue[0], font=("Arial", 10)).grid(row=row, column=0, padx=5, pady=5)  # Venue ID
               tk.Label(table_frame, text=venue[1], font=("Arial", 10)).grid(row=row, column=1, padx=5, pady=5)  # Venue Name
               tk.Label(table_frame, text=venue[2], font=("Arial", 10)).grid(row=row, column=2, padx=5, pady=5)  # Address
               tk.Label(table_frame, text=venue[3], font=("Arial", 10)).grid(row=row, column=3, padx=5, pady=5)  # Capacity
               tk.Label(table_frame, text=venue[4], font=("Arial", 10)).grid(row=row, column=4, padx=5, pady=5)  # Event ID
               tk.Label(table_frame, text=venue[5], font=("Arial", 10)).grid(row=row, column=5, padx=5, pady=5)  # Event Date

               update_button = tk.Button(table_frame, text="Update", command=lambda vid=venue[0]: update_venue_window(vid, venue_window))
               update_button.grid(row=row, column=6, padx=5, pady=5)

               delete_button = tk.Button(table_frame, text="Delete", command=lambda vid=venue[0]: delete_venue(vid, venue_window))
               delete_button.grid(row=row, column=7, padx=5, pady=5)
        else:
            tk.Label(table_frame, text="No venues found for this event.", font=("Arial", 10)).grid(row=1, column=0, columnspan=8, padx=5, pady=5)


        table_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        if db.is_connected():
            db.close()

def add_venue_window(event_id):
    add_window = Toplevel(root)
    add_window.title("Add Venue")
    add_window.geometry("300x400")

    name_var = StringVar()
    address_var = StringVar()
    capacity_var = StringVar()

    # Retrieve the event_date for the selected event_id from the events table
    event_date = None
    try:
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT event_date FROM events WHERE event_id = %s", (event_id,))
        event_date_result = cursor.fetchone()
        if event_date_result:
            event_date = event_date_result[0]  # Get the event_date from the query result
        else:
            messagebox.showerror("Error", "No event found with the given event ID.")
            add_window.destroy()
            return  # Exit if no valid event_date is found
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error fetching event date: {err}")
        add_window.destroy()
        return
    finally:
        if db.is_connected():
            db.close()

    # Set up the form to add venue details
    Label(add_window, text="Venue Name:").pack(pady=5)
    name_entry = Entry(add_window, textvariable=name_var)
    name_entry.pack(pady=5)

    Label(add_window, text="Address:").pack(pady=5)
    address_entry = Entry(add_window, textvariable=address_var)
    address_entry.pack(pady=5)

    Label(add_window, text="Capacity:").pack(pady=5)
    capacity_entry = Entry(add_window, textvariable=capacity_var)
    capacity_entry.pack(pady=5)

    submit_add_btn = tk.Button(add_window, text="Add Venue", command=lambda: add_venue(event_id, event_date, name_var.get(), address_var.get(), capacity_var.get(), add_window))
    submit_add_btn.pack(pady=20)

# Function to add venue to the database
def add_venue(event_id, event_date, name, address, capacity, window):
    try:
        db = connect_db()
        cursor = db.cursor()
        
        # Insert into venue table with event_date fetched automatically
        insert_query = "INSERT INTO venue (venue_name, address, capacity, event_id, event_date) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (name, address, capacity, event_id, event_date))

        trigger_sql = """
          CREATE TRIGGER IF NOT EXISTS before_insert_venue
          BEFORE INSERT ON venue
          FOR EACH ROW
          BEGIN
              -- Check if there is already a venue for the given event_id
          IF EXISTS (SELECT 1 FROM venue WHERE event_id = NEW.event_id) THEN
          SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Each event can only have one venue.';
          END IF;

              -- Check if a venue with the same name and address exists for the same event_date
          IF EXISTS (
             SELECT 1 FROM venue 
             WHERE venue_name = NEW.venue_name 
             AND address = NEW.address 
             AND event_date = NEW.event_date
          ) THEN
             SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'A venue with the same name, address, and event date already exists.';
          END IF;
          END;
         """

    

        # Attempt to create the trigger
        cursor.execute(trigger_sql)
        
        db.commit()
        messagebox.showinfo("Success", "Venue added successfully!")
        window.destroy()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        if db.is_connected():
            db.close()

# Function to add venue to the database
def add_venue(event_id, event_date, name, address, capacity, window):
    try:
        db = connect_db()
        cursor = db.cursor()
        
        # Insert into venue table with event_date fetched automatically
        insert_query = "INSERT INTO venue (venue_name, address, capacity, event_id, event_date) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (name, address, capacity, event_id, event_date))

        trigger_sql = """
          CREATE TRIGGER IF NOT EXISTS before_insert_venue
          BEFORE INSERT ON venue
          FOR EACH ROW
          BEGIN
              -- Check if there is already a venue for the given event_id
          IF EXISTS (SELECT 1 FROM venue WHERE event_id = NEW.event_id) THEN
          SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Each event can only have one venue.';
          END IF;

              -- Check if a venue with the same name and address exists for the same event_date
          IF EXISTS (
             SELECT 1 FROM venue 
             WHERE venue_name = NEW.venue_name 
             AND address = NEW.address 
             AND event_date = NEW.event_date
          ) THEN
             SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'A venue with the same name, address, and event date already exists.';
          END IF;
          END;
         """

        # Attempt to create the trigger
        cursor.execute(trigger_sql)
        
        db.commit()
        messagebox.showinfo("Success", "Venue added successfully!")
        window.destroy()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        if db.is_connected():
            db.close()

# Function to update venue window
def update_venue_window(venue_id, venue_window):
    update_window = Toplevel(venue_window)
    update_window.title("Update Venue")
    update_window.geometry("300x400")

    name_var = StringVar()
    address_var = StringVar()
    capacity_var = StringVar()

    try:
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT venue_name, address, capacity FROM venue WHERE venue_id = %s", (venue_id,))
        venue = cursor.fetchone()

        if venue:
            name_var.set(venue[0])
            address_var.set(venue[1])
            capacity_var.set(venue[2])
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        if db.is_connected():
            db.close()
            

    Label(update_window, text="Venue Name:").pack(pady=5)
    name_entry = Entry(update_window, textvariable=name_var)
    name_entry.pack(pady=5)

    Label(update_window, text="Address:").pack(pady=5)
    address_entry = Entry(update_window, textvariable=address_var)
    address_entry.pack(pady=5)

    Label(update_window, text="Capacity:").pack(pady=5)
    capacity_entry = Entry(update_window, textvariable=capacity_var)
    capacity_entry.pack(pady=5)

    update_button = tk.Button(update_window, text="Update Venue", command=lambda: update_venue(venue_id, name_var.get(), address_var.get(), capacity_var.get(), update_window))
    update_button.pack(pady=20)

# Function to update venue in the database
def update_venue(venue_id, name, address, capacity, window):
    try:
        db = connect_db()
        cursor = db.cursor()
        update_query = "UPDATE venue SET venue_name = %s, address = %s, capacity = %s WHERE venue_id = %s"
        cursor.execute(update_query, (name, address, capacity, venue_id))
        db.commit()
        messagebox.showinfo("Success", "Venue updated successfully!")
        window.destroy()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        if db.is_connected():
            db.close()
        

# Function to delete venue
def delete_venue(venue_id, venue_window):
    try:
        db = connect_db()
        cursor = db.cursor()
        delete_query = "DELETE FROM venue WHERE venue_id = %s"
        cursor.execute(delete_query, (venue_id,))
        db.commit()
        messagebox.showinfo("Success", "Venue deleted successfully!")
        venue_window.destroy()  
        display_venue_details(venue_window, venue_window.winfo_children()[0].event_id)  # Refresh the venue details
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        if db.is_connected():
            db.close()

def clear_screen():
    """Clears all widgets from the main window."""
    for widget in root.winfo_children():
        widget.place_forget()

# GUI Setup
root = tk.Tk()
root.geometry("600x400")
root.title("Event Management System")

# Initial Buttons
admin_login_btn = tk.Button(root, text="Admin Login", bg='blue', command=show_login_fields)
admin_login_btn.place(x=50, y=50, width=100)

register_btn = tk.Button(root, text="Register", bg='green', command=register_page)
register_btn.place(x=160, y=50, width=100)

event_schedule_btn = tk.Button(root, text="Event Schedule", bg='purple', command=display_event_schedule)
event_schedule_btn.place(x=270, y=50, width=120)

# head_id and password fields (initially hidden)
lbl_head_id = tk.Label(root, text="Head ID -")
head_id_entry = tk.Entry(root, width=35)

lbl_password = tk.Label(root, text="Password -")
password_entry = tk.Entry(root, width=35, show='*')

# Submit button for login (initially hidden)
submit_btn = tk.Button(root, text="Submit", command=admin_login)

root.mainloop()

