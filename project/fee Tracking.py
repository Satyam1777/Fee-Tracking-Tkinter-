import mysql.connector as myconn
from tkinter import *
from tkinter import ttk, messagebox
from tkinter.font import Font
from tkinter import Toplevel, Label, Button, PhotoImage, Canvas, Frame
from PIL import Image, ImageTk
# Global variables for student data
student_name = ""
student_rollno = ""

def hover_button(e, button, color):
    button.config(bg=color)

def leave_button(e, button, color):
    button.config(bg=color)
    
def login_func():
    global student_name, student_rollno
    if name_entry.get() == "Enter Name" or rollno_entry.get() == "Enter Roll No":
        messagebox.showerror("Error!", "All fields are required")
    else:
        try:
            connection = myconn.connect(host="localhost", user="root", password="root", database="student_fees_tracking")
            cur = connection.cursor()
            cur.execute("SELECT student_name, roll_no, fees_paid FROM student_fees_tracking.record WHERE student_name=%s AND roll_no=%s", 
                        (name_entry.get(), rollno_entry.get()))
            row = cur.fetchone()
            
            if row is None:
                messagebox.showerror("Error!", "Invalid USERNAME & PASSWORD")
            else:
                # Save the student details
                student_name = row[0]
                student_rollno = row[1]
                # Open status window if login is successful
                open_status_window(row[2] ,row[0] , row[1] )
            connection.close()
        except Exception as e:
            messagebox.showerror("Error!", f"Error due to {str(e)}")

def pay_fees():
    try:
        global student_name, student_rollno
        connection = myconn.connect(host="localhost", user="root", password="root", database="student_fees_tracking")
        cur = connection.cursor()
        
        print(f"Updating fees for Name: {student_name}, Roll No: {student_rollno}")
        cur.execute("UPDATE record SET fees_paid=1 WHERE student_name=%s AND roll_no=%s", (student_name, student_rollno))
        connection.commit()  
        
        messagebox.showinfo("Success", "Fees paid successfully")
    except Exception as e:
        print(f"Error during payment: {str(e)}")  
        messagebox.showerror("Error!", f"Error due to {str(e)}")
    finally:
        if connection.is_connected():
            connection.close()

def on_enter(e, entry, placeholder):
    if entry.get() == placeholder:
        entry.delete(0, "end")
        entry.config(fg="black")

def on_leave(e, entry, placeholder):
    if entry.get() == "":
        entry.insert(0, placeholder)
        entry.config(fg="grey")

def hover_button(e, button, color):
    button.config(bg=color)

def open_status_window(fees_status, student_name, roll_no):


    # Create a new Toplevel window
    status_window = Toplevel()
    status_window.title("Student Fees Status")
    status_window.geometry("600x500")
    status_window.config(bg="#f4f4f4")

    # Custom font
    header_font = Font(family="Helvetica", size=18, weight="bold")
    text_font = Font(family="Helvetica", size=14)
    button_font = Font(family="Helvetica", size=12, weight="bold")

    # Canvas for gradient header
    canvas = Canvas(status_window, width=600, height=80, highlightthickness=0)
    canvas.pack()
    canvas.create_rectangle(0, 0, 600, 80, fill="#007ACC", outline="")
    canvas.create_text(300, 40, text="Fees Status", fill="white", font=header_font)

    # Student Name and Roll No
    Label(
        status_window,
        text=f"Name: {student_name}",
        font=text_font,
        bg="#f4f4f4",
        fg="#333",
    ).pack(pady=10)

    Label(
        status_window,
        text=f"Roll No: {roll_no}",
        font=text_font,
        bg="#f4f4f4",
        fg="#333",
    ).pack(pady=5)

    # Determine status and load the appropriate image and message
    if fees_status == 1:  # Fees Paid
        image_path = r"C:\Users\Dell\OneDrive\Desktop\project\paid.png"
        status_message = "Fees Paid Successfully!"
        status_color = "#28a745"  # Green
        show_pay_button = False
    else:  # Fees Unpaid
        image_path = r"C:\Users\Dell\OneDrive\Desktop\project\unpaid-removebg-preview.png"
        status_message = "Fees Not Paid!"
        status_color = "#dc3545"  # Red
        show_pay_button = True

    # Load and display the status image
    try:
        status_image = Image.open(image_path)
        status_image = status_image.resize((150, 150), Image.ANTIALIAS)
        status_photo = ImageTk.PhotoImage(status_image)
        Label(status_window, image=status_photo, bg="#f4f4f4").pack(pady=20)
        status_window.status_photo = status_photo  # Prevent garbage collection
    except Exception as e:
        Label(
            status_window,
            text="(Image not found)",
            font=text_font,
            bg="#f4f4f4",
            fg=status_color,
        ).pack(pady=20)

    # Display status message
    Label(
        status_window,
        text=status_message,
        font=("Helvetica", 16, "bold"),
        bg="#f4f4f4",
        fg=status_color,
    ).pack(pady=10)

    # Add "Pay Now" button if fees are unpaid
    if show_pay_button:
        Button(
            status_window,
            text="Pay Now",
            command=pay_fees,
            font=button_font,
            bg="#dc3545",  # Red background for attention
            fg="white",
            cursor="hand2",
            activebackground="#c82333",
            activeforeground="white",
            width=12,
            height=1,
        ).pack(pady=10)

    # Add Close Button
    Button(
        status_window,
        text="Close",
        command=status_window.destroy,
        font=button_font,
        bg="#007ACC",
        fg="white",
        cursor="hand2",
        activebackground="#005F9E",
        activeforeground="white",
        width=12,
        height=1,
    ).pack(pady=20)

    status_window.mainloop()

# Admin Login Functionality
# Admin Login Functionality
def open_admin_window():
    # Create the admin login window
    admin_window = Toplevel(root)
    admin_window.title("Admin Login")
    admin_window.geometry("400x350")
    admin_window.config(bg="#f0f0f0")  # Light background color

    # Title label
    Label(admin_window, text="Admin Login", font=("Helvetica", 24, "bold"), bg="#f0f0f0", fg="#333333").place(x=110, y=20)

    # Admin ID label and entry
    Label(admin_window, text="Admin ID", font=("Helvetica", 15), bg="#f0f0f0", fg="#555555").place(x=50, y=80)
    admin_id = Entry(admin_window, font=("Arial", 14), bg="#ffffff", fg="#333333", relief=SOLID, bd=1)
    admin_id.place(x=50, y=110, width=300, height=30)

    # Password label and entry
    Label(admin_window, text="Password", font=("Helvetica", 15), bg="#f0f0f0", fg="#555555").place(x=50, y=150)
    admin_password = Entry(admin_window, font=("Arial", 14), bg="#ffffff", fg="#333333", show="*", relief=SOLID, bd=1)
    admin_password.place(x=50, y=180, width=300, height=30)

    # Admin login function
    def admin_login():
        if admin_id.get() == "" or admin_password.get() == "":
            messagebox.showerror("Error!", "All fields are required")
        else:
            try:
                connection = myconn.connect(host="localhost", user="root", password="root", database="student_fees_tracking")
                cur = connection.cursor()
                cur.execute("SELECT * FROM admin WHERE id=%s AND password=%s", (admin_id.get(), admin_password.get()))
                row = cur.fetchone()
                
                if row is None:
                    messagebox.showerror("Error!", "Invalid Admin ID or Password")
                else:
                    messagebox.showinfo("Success", "Welcome Admin!")
                    admin_window.destroy()
                    open_admin_dashboard()
            except Exception as e:
                messagebox.showerror("Error!", f"Error due to {str(e)}")
            finally:
                if connection.is_connected():
                    connection.close()

    # Button hover effect
    def on_enter(e):
        login_button['bg'] = "#3578e5"  # Darker shade for hover

    def on_leave(e):
        login_button['bg'] = "#4a90e2"  # Original color

    # Login Button with hover effect
    login_button = Button(admin_window, text="Log In", command=admin_login, font=("Arial", 14, "bold"), bd=0, 
                          bg="#4a90e2", fg="white", cursor="hand2", activebackground="#3578e5", activeforeground="white")
    login_button.place(x=50, y=230, width=300, height=40)
    login_button.bind("<Enter>", on_enter)
    login_button.bind("<Leave>", on_leave)

    # Close Button
    Button(admin_window, text="Close", command=admin_window.destroy, font=("Arial", 14, "bold"), bd=0, 
           bg="red", fg="white", cursor="hand2", activebackground="darkred", activeforeground="white").place(x=50, y=280, width=300, height=40)

def open_admin_dashboard():
    dashboard = Tk()
    dashboard.title("Admin Dashboard")
    dashboard.geometry("900x650")
    dashboard.config(bg="#f0f8ff")

    # Title
    Label(dashboard, text="Admin Dashboard", font=("Arial", 24, "bold"), bg="#f0f8ff", fg="#2a52be").pack(pady=10)

    # Create a frame for the Treeview widget
    table_frame = Frame(dashboard, bg="white", relief=RIDGE, bd=2)
    table_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

    # Scrollbars
    scroll_x = Scrollbar(table_frame, orient=HORIZONTAL)
    scroll_y = Scrollbar(table_frame, orient=VERTICAL)

    # Treeview widget for displaying records
    record_table = ttk.Treeview(table_frame, columns=("roll_no", "student_name", "fees_paid"),
                                xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
    scroll_x.pack(side=BOTTOM, fill=X)
    scroll_y.pack(side=RIGHT, fill=Y)
    scroll_x.config(command=record_table.xview)
    scroll_y.config(command=record_table.yview)

    record_table.heading("roll_no", text="Roll No")
    record_table.heading("student_name", text="Student Name")
    record_table.heading("fees_paid", text="Fees Paid")
    record_table['show'] = 'headings'
    record_table.column("roll_no", width=100)
    record_table.column("student_name", width=200)
    record_table.column("fees_paid", width=100)
    record_table.pack(fill=BOTH, expand=True)

    # Adding alternating row colors for readability
    style = ttk.Style()
    style.configure("Treeview", rowheight=25)
    style.map("Treeview", background=[('selected', '#c0c0c0')])
    style.configure("Treeview.Heading", font=("Arial", 12, "bold"))
    
    def fetch_data():
        for i in record_table.get_children():
            record_table.delete(i)
        
        try:
            connection = myconn.connect(host="localhost", user="root", password="root", database="student_fees_tracking")
            cur = connection.cursor()
            cur.execute("SELECT roll_no, student_name, fees_paid FROM record")
            rows = cur.fetchall()
            for idx, row in enumerate(rows):
                tag = 'even' if idx % 2 == 0 else 'odd'
                record_table.insert("", END, values=row, tags=(tag,))
            record_table.tag_configure('even', background='#f2f2f2')
            record_table.tag_configure('odd', background='#ffffff')
            connection.close()
        except Exception as e:
            messagebox.showerror("Error!", f"Error due to {str(e)}")

    fetch_data()

    # Form to Add a New Student
    add_frame = Frame(dashboard, bg="#f0f8ff")
    add_frame.pack(fill=X, padx=20, pady=10)

    Label(add_frame, text="Roll No:", font=("Arial", 12), bg="#f0f8ff").grid(row=0, column=0, padx=5, pady=5, sticky=W)
    add_rollno = Entry(add_frame, font=("Arial", 12), bg="lightgray")
    add_rollno.grid(row=0, column=1, padx=5, pady=5)

    Label(add_frame, text="Name:", font=("Arial", 12), bg="#f0f8ff").grid(row=0, column=2, padx=5, pady=5, sticky=W)
    add_name = Entry(add_frame, font=("Arial", 12), bg="lightgray")
    add_name.grid(row=0, column=3, padx=5, pady=5)

    Label(add_frame, text="Fees Paid (0/1):", font=("Arial", 12), bg="#f0f8ff").grid(row=0, column=4, padx=5, pady=5, sticky=W)
    add_fees_paid = Entry(add_frame, font=("Arial", 12), bg="lightgray")
    add_fees_paid.grid(row=0, column=5, padx=5, pady=5)

    def add_student():
        rollno = add_rollno.get()
        name = add_name.get()
        fees_paid = add_fees_paid.get()
        if rollno == "" or name == "" or fees_paid == "":
            messagebox.showerror("Error", "All fields are required")
            return
        try:
            connection = myconn.connect(host="localhost", user="root", password="root", database="student_fees_tracking")
            cur = connection.cursor()
            cur.execute("INSERT INTO record (roll_no, student_name, fees_paid) VALUES (%s, %s, %s)", (rollno, name, fees_paid))
            connection.commit()
            connection.close()
            messagebox.showinfo("Success", "Student added successfully")
            fetch_data()
            add_rollno.delete(0, END)
            add_name.delete(0, END)
            add_fees_paid.delete(0, END)
        except Exception as e:
            messagebox.showerror("Error", f"Error due to {str(e)}")

    add_button = Button(add_frame, text="Add Student", command=add_student, font=("Arial", 12), bg="#32cd32", fg="white")
    add_button.grid(row=0, column=6, padx=10, pady=5)

    def delete_student():
        selected_item = record_table.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a student to delete")
            return
        rollno = record_table.item(selected_item)['values'][0]
        
        try:
            connection = myconn.connect(host="localhost", user="root", password="root", database="student_fees_tracking")
            cur = connection.cursor()
            cur.execute("DELETE FROM record WHERE roll_no=%s", (rollno,))
            connection.commit()
            connection.close()
            messagebox.showinfo("Success", "Student deleted successfully")
            fetch_data()
        except Exception as e:
            messagebox.showerror("Error", f"Error due to {str(e)}")

    delete_button = Button(dashboard, text="Delete Student", command=delete_student, font=("Arial", 12), bg="#ff6347", fg="white")
    delete_button.pack(pady=10)

    close_button = Button(dashboard, text="Close", command=dashboard.destroy, font=("Arial", 12), bg="#b22222", fg="white")
    close_button.pack(pady=10)

    # Adding hover effects for buttons
    for button in [add_button, delete_button, close_button]:
        button.bind("<Enter>", lambda e, b=button: b.config(bg="darkgrey"))
        button.bind("<Leave>", lambda e, b=button: b.config(bg=b.cget("bg")))

    dashboard.mainloop()


# Main login window

root = Tk()
root.title("Student Fees Tracking System")
root.geometry("1280x800+0+0")
root.config(bg="white")

# Gradient Background
background_frame = Canvas(root, width=1280, height=800)
background_frame.create_rectangle(0, 0, 1280, 800, fill="#6dd5fa", outline="")
background_frame.create_rectangle(0, 400, 1280, 800, fill="#2980b9", outline="")
background_frame.pack(fill="both", expand=True)

# Header Section
header_frame = Frame(root, bg="#007ACC", height=100)
header_frame.pack(fill=X)

header_label = Label(
    header_frame, 
    text="Student Fees Tracking System", 
    font=("Helvetica", 30, "bold"), 
    bg="#007ACC", 
    fg="white"
)
header_label.pack(pady=20)

# Center Content Frame
content_frame = Frame(root, bg="white", relief=SOLID, bd=1)
content_frame.place(x=200, y=150, width=880, height=500)

# Left Section - Login Card
frame_left = Frame(content_frame, bg="#f5f5f5", relief=RIDGE, bd=2)
frame_left.place(x=50, y=50, width=350, height=400)

Label(frame_left, text="Sign In", font=("Helvetica", 24, "bold"), bg="#f5f5f5", fg="#007ACC").pack(pady=20)

# Name Entry
name_entry = Entry(frame_left, font=("Helvetica", 15), fg="grey", bg="#ffffff", relief=SOLID, bd=1)
name_entry.insert(0, "Enter Name")
name_entry.bind("<FocusIn>", lambda e: name_entry.delete(0, "end"))
name_entry.pack(pady=10, ipady=8, padx=20, fill=X)

# Roll Number Entry
rollno_entry = Entry(frame_left, font=("Helvetica", 15), fg="grey", bg="#ffffff", relief=SOLID, bd=1)
rollno_entry.insert(0, "Enter Roll No")
rollno_entry.bind("<FocusIn>", lambda e: rollno_entry.delete(0, "end"))
rollno_entry.pack(pady=10, ipady=8, padx=20, fill=X)

# Login Button
login_button = Button(
    frame_left, 
    text="Log In", 
    font=("Helvetica", 15, "bold"), 
    bg="#007ACC", 
    fg="white", 
    bd=0, 
    cursor="hand2", 
    relief=SOLID,
    command=login_func  # Bind login_func to the button
)
login_button.pack(pady=20, ipadx=10, ipady=10)
login_button.bind("<Enter>", lambda e: hover_button(e, login_button, "#0056A6"))
login_button.bind("<Leave>", lambda e: leave_button(e, login_button, "#007ACC"))

# Admin Login Button
admin_button = Button(
    frame_left, 
    text="Admin Login", 
    font=("Helvetica", 15, "bold"), 
    bg="#28A745", 
    fg="white", 
    bd=0, 
    cursor="hand2", 
    relief=SOLID,
    command=open_admin_window  # Ensure this points to open_admin_window
)

admin_button.pack(pady=10, ipadx=10, ipady=10)
admin_button.bind("<Enter>", lambda e: hover_button(e, admin_button, "#1E7A36"))
admin_button.bind("<Leave>", lambda e: leave_button(e, admin_button, "#28A745"))

# Right Section - Image or Welcome Text
frame_right = Frame(content_frame, bg="#ffffff")
frame_right.place(x=450, y=50, width=410, height=400)

# Add an Image
image = Image.open(r"C:\Users\Dell\OneDrive\Desktop\project\login.png")
 # Replace with an actual image file
image = image.resize((300, 200), Image.Resampling.LANCZOS)

photo = ImageTk.PhotoImage(image)

image_label = Label(frame_right, image=photo, bg="white")
image_label.image = photo
image_label.pack(pady=20)

welcome_label = Label(
    frame_right, 
    text="Welcome to \nStudent Fees Tracking System", 
    font=("Helvetica", 20, "bold"), 
    bg="#ffffff", 
    fg="#007ACC"
)
welcome_label.pack(pady=20)

# Footer
footer_frame = Frame(root, bg="#007ACC", height=50)
footer_frame.pack(fill=X, side=BOTTOM)

footer_label = Label(
    footer_frame, 
    text="© 2024 Student Fees Tracking System | All Rights Reserved", 
    font=("Helvetica", 12), 
    bg="#007ACC", 
    fg="white"
)
footer_label.pack(pady=10)

root.mainloop()
