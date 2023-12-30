import re
import tkinter as tk
from tkinter import messagebox
import pymysql
from tkinter import *
from datetime import datetime


def clear_entries_2():
    first_name_entry_1.delete(0, END)
    last_name_entry_1.delete(0, END)
    dob_entry.delete(0, END)
    aadhar_entry.delete(0, END)
    selectParty_entry.delete(0, END)


def Vote_ME_DB():
    if first_name_entry_1.get() == '' or last_name_entry_1.get() == '' or dob_entry.get() == '' or aadhar_entry.get() == '' or selectParty_entry.get() == '':
        messagebox.showerror('Entry Error', 'All fields are required')
    elif any(char.isdigit() for char in first_name_entry.get()) or any(
            char.isdigit() for char in last_name_entry.get()):
        messagebox.showerror('Digit Error', 'Digits are not allowed in Names')
    elif len(aadhar_entry.get()) != 12 or not aadhar_entry.get().isdigit():
        messagebox.showerror('Aadhar error', 'Please enter a valid 12-digit Aadhar number')
    elif len(dob_entry.get()) != 10 or not re.match(r'\d{4}-\d{2}-\d{2}', dob_entry.get()):
        messagebox.showerror('DOB Error', 'Please enter the date of birth in YYYY-MM-DD format')
    elif selectParty_entry.get().isdigit():
        messagebox.showerror('Party enter error', 'Only strings are allowed for the party')
    elif selectParty_entry.get() == 'BJP':
        messagebox.showinfo('Success', 'Welcome to our Party')
    else:
        try:
            con = pymysql.connect(host='localhost', user='root', password='#Mtboss123', database='userdata')
            mycursor = con.cursor()
        except:
            messagebox.showerror('Connection error', 'Database connectivity issue')
            return

        dob = datetime.strptime(dob_entry.get(), '%Y-%m-%d')
        today = datetime.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

        if age < 18:
            messagebox.showerror('Age Error', 'You must be at least 18 years old to vote')
        else:
            # Check if the user with the same Aadhar number already voted
            query = 'SELECT * FROM data WHERE aadharnumber=%s'
            mycursor.execute(query, (aadhar_entry.get(),))
            row = mycursor.fetchone()
            if row:
                messagebox.showerror('Already Voted', 'You have already voted with this Aadhar number')
            else:
                # Insert the user's vote into the database
                query = 'INSERT INTO data(aadharnumber, dob, parties) VALUES (%s, %s, %s)'
                mycursor.execute(query, (aadhar_entry.get(), dob_entry.get(), selectParty_entry.get()))
                con.commit()
                con.close()
                messagebox.showinfo('Success', 'Your Vote is submitted successfully')
                clear_entries_2()


def Forget_Button():
    def clear_entries_1():
        EmailLabel_Entry.delete(0, END)
        passwordEntry.delete(0, END)

    def change_password():
        if EmailLabel_Entry.get() == '' or passwordEntry.get() == '':
            messagebox.showerror('Error', 'All Fields are required', parent=window)
        elif len(passwordEntry.get()) < 8:
            messagebox.showerror('Password error', 'Password must be 8 character long')
        else:
            con = pymysql.connect(host='localhost', user='root', password='', database='userdata')
            mycursor = con.cursor()
            query = 'select * from data where email=%s'
            mycursor.execute(query, EmailLabel_Entry.get())
            row = mycursor.fetchone()
            if row == None:
                messagebox.showerror('E-mail error', 'Incorrect E-mail', parent=window)
            else:
                query = 'update data set password=%s where email=%s'
                mycursor.execute(query, (passwordEntry.get(), EmailLabel_Entry.get()))
                con.commit()
                con.close()
                messagebox.showinfo('Success', 'Password rest is successful', parent=window)
                window.destroy()
                clear_entries_1()

    window = Toplevel(bg='black')
    window.title('Change Password')
    window.geometry('300x400')

    heading_label = Label(window, bg='black', text='RESET PASSWORD', font=('Arial', '16', 'bold'), fg='magenta2')
    heading_label.place(x=45, y=45)

    emailLabel = Label(window, bg='black', text='E-Mail:', font=('Arial', '13', 'bold'), fg='magenta2')
    emailLabel.place(x=25, y=110)
    EmailLabel_Entry = Entry(window, bd='0', bg='white')
    EmailLabel_Entry.grid(padx=130, pady=115)

    passwordLabel = Label(window, bg='black', text='NewPassword:', font=('Arial', '13', 'bold'), fg='magenta2')
    passwordLabel.place(x=6, y=245)
    passwordEntry = Entry(window, bd='0', bg='white', show='*')
    passwordEntry.grid(column=0, row=1)

    Reset_button = tk.Button(window, cursor='hand2', text='RESET PASSWORD', bg='green', fg='yellow', font='Arial',
                             command=change_password
                             )
    Reset_button.place(x=55, y=345)

    window.mainloop()


def clear_entries():
    First_name_entry_2.delete(0, END)
    pass_entry.delete(0, END)
    email_entry.delete(0, END)
    first_name_entry.delete(0, END)
    last_name_entry.delete(0, END)
    password_entry.delete(0, END)
    confirm_password_entry.delete(0, END)
    check.set(0)


def Sign_UP_DB():
    try:
        if password_entry.get() != confirm_password_entry.get():
            messagebox.showerror('Error', 'Password wont match')
        elif first_name_entry.get() == '' or last_name_entry.get() == '' or email_entry.get() == '' or password_entry.get() == '' or confirm_password_entry.get() == '':
            messagebox.showerror('Entry Error', 'All Fields are required')
        elif len(password_entry.get()) < 8:
            messagebox.showerror('Password error', 'Password must be 8 character long')
        elif any(char.isdigit() for char in first_name_entry.get()) or any(
                char.isdigit() for char in last_name_entry.get()):
            messagebox.showerror('Digit Error', 'Digits are not allowed in Names')
        elif check.get() == 0:
            messagebox.showerror('Check error', 'Please accept Terms & Conditions')
        elif not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email_entry.get()):
            messagebox.showerror('E-mail error', 'Please enter a valid email address')
        else:
            try:
                # Adjust the MySQL connection parameters
                con = pymysql.connect(
                    host='localhost',  # Replace with your MySQL host
                    user='root',  # Replace with your MySQL user
                    password='#Mtboss123',  # Replace with your MySQL password
                )
                mycursor = con.cursor()
            except pymysql.Error as e:
                messagebox.showerror('Error', 'Database connectivity error: ' + str(e))
                return

            try:
                # Create the "userdata" database if it doesn't exist
                create_db_query = 'CREATE DATABASE IF NOT EXISTS userdata'
                mycursor.execute(create_db_query)

                # Select the "userdata" database
                use_db_query = 'USE userdata'
                mycursor.execute(use_db_query)
                # Create the "data" table
                create_table_query = 'CREATE TABLE IF NOT EXISTS data(id INT AUTO_INCREMENT PRIMARY KEY NOT NULL, email VARCHAR(50), firstname VARCHAR(100), lastname VARCHAR(100), password VARCHAR(20))'
                mycursor.execute(create_table_query)

            except pymysql.Error as e:
                messagebox.showerror('MySQL Error', 'Error creating table: ' + str(e))

            query = 'select * from data where firstname=%s'
            mycursor.execute(query, (first_name_entry.get()))
            row = mycursor.fetchone()
            if row != None:
                messagebox.showerror('Userdata Error', 'Userdata Already exist pls try to Login')
            else:
                query = 'insert into data(email, firstname, lastname, password) values(%s,%s,%s,%s)'
                mycursor.execute(query,
                                 (email_entry.get(), first_name_entry.get(), last_name_entry.get(),
                                  password_entry.get()))
                con.commit()
                con.close()
                messagebox.showinfo('Success', 'Registration is successful')
                clear_entries()
                switch_page(2)

    except:
        return 'success'


def Connect_DB():
    if First_name_entry_2.get() == '' or pass_entry.get() == '':
        messagebox.showerror('Error', 'All Fields are required')
    else:
        try:
            con = pymysql.connect(host='localhost', user='root', password='#Mtboss123')
            mycursor = con.cursor()
        except:
            messagebox.showerror('Connection error', 'Database connectivity issue')
            return
        query = 'USE userdata'
        mycursor.execute(query)
        query = 'select * from data where firstname=%s and password=%s'
        mycursor.execute(query, (First_name_entry_2.get(), pass_entry.get()))
        row = mycursor.fetchone()
        if row == None:
            messagebox.showerror('Login Error', 'Invalid username or password')
        else:
            messagebox.showinfo('Login Success', 'Login is Success! Welcome sir')
            switch_page(1)
        con.close()
        clear_entries()


def Login_Page_from_SignUp_page():
    return switch_page(2)


def SignUp_page_to_Login_Page():
    return switch_page(3)


# Function to switch to a specific page
def switch_page(page_index):
    # Hide all pages
    for page in pages:
        page.pack_forget()
    # Show the selected page
    pages[page_index].pack(fill='both', expand=True)


# function to click button to switch the page
def on_button_click(option):
    print(f"{option} button clicked")
    if option == "Home":
        switch_page(0)  # Switch to the Home page
    elif option == "VoteMe":
        switch_page(1)  # Switch to the VoteMe page
    elif option == 'Login':
        switch_page(2)
    elif option == 'Signup':
        switch_page(3)
    elif option == 'About Us':
        switch_page(4)
    elif option == 'Contact Us':
        switch_page(5)
    else:
        switch_page(0), switch_page(1), switch_page(2), switch_page(3), switch_page(4), switch_page(5)
    # Add more conditions for other pages as needed


root = tk.Tk()
root.title('VoteMe')
root.geometry('800x400+180+130')

# Create a list to store references to all the pages/frames
pages = []

# Create a frame with a red background for the sidebar
sidebar_frame = tk.Frame(root, bg='red', width=200, pady=3)
sidebar_frame.pack(side='left', fill='y')

# Create buttons to serve as the sidebar options
options = ["Home", "VoteMe", "Login", "Signup", "About Us", "Contact Us"]

for option in options:
    button = tk.Button(sidebar_frame, height=3, text=option.upper(), width=20,
                       command=lambda o=option: on_button_click(o))
    button.pack(fill='x', pady=15)

# Create separate frames for each page/section
home_frame = tk.Frame(root)
pages.append(home_frame)

voteme_frame = tk.Frame(root)
pages.append(voteme_frame)

login_frame = tk.Frame(root)
pages.append(login_frame)

signup_frame = tk.Frame(root)
pages.append(signup_frame)

about_us_frame = tk.Frame(root)
pages.append(about_us_frame)

contact_Us = tk.Frame(root)
pages.append(contact_Us)

# Content for the Signup Page
signup_label = tk.Label(signup_frame, text='Sign Up', font=('Arial', 20), fg='firebrick1')
signup_label.grid(row=0, column=0, columnspan=2, pady=10)

first_name_label = tk.Label(signup_frame, text='First Name:', font='Arial')
first_name_label.grid(row=1, column=0, padx=10, pady=5, sticky='w')

first_name_entry = tk.Entry(signup_frame, bd='0', bg='white')
first_name_entry.grid(row=1, column=1, padx=10, pady=5)

last_name_label = tk.Label(signup_frame, text='Last Name:', font='Arial')
last_name_label.grid(row=2, column=0, padx=10, pady=5, sticky='w')

last_name_entry = tk.Entry(signup_frame, bd='0', bg='white')
last_name_entry.grid(row=2, column=1, padx=10, pady=5)

email_label = tk.Label(signup_frame, text='Email Address:', font='Arial')
email_label.grid(row=3, column=0, padx=10, pady=5, sticky='w')

email_entry = tk.Entry(signup_frame, bd='0', bg='white')
email_entry.grid(row=3, column=1, padx=10, pady=5)

password_label = tk.Label(signup_frame, text='Password:', font='Arial')
password_label.grid(row=4, column=0, padx=10, pady=5, sticky='w')

password_entry = tk.Entry(signup_frame, bd='0', bg='white', show='*')  # Mask the password
password_entry.grid(row=4, column=1, padx=10, pady=5)

confirm_password_label = tk.Label(signup_frame, text='Confirm Password:', font='Arial')
confirm_password_label.grid(row=5, column=0, padx=10, pady=5, sticky='w')

confirm_password_entry = tk.Entry(signup_frame, bd='0', bg='white', show='*')  # Mask the password
confirm_password_entry.grid(row=5, column=1, padx=10, pady=5)

check = tk.IntVar()
terms_and_conditions = tk.Checkbutton(signup_frame, cursor='hand2', text='I agree to Terms & Conditions', font='Arial',
                                      fg='blue', variable=check)
terms_and_conditions.grid(row=6)

signup_button = tk.Button(signup_frame, cursor='hand2', text='Sign Up', bg='green', fg='yellow', font='Arial',
                          command=Sign_UP_DB
                          )
signup_button.grid(row=7, column=0, pady=10)

Already_accounted = tk.Label(signup_frame, text='Already have an account?', font='Arial', fg='firebrick1', )
Already_accounted.grid(row=9, column=0)

Login_Redirect_Button = tk.Button(signup_frame, cursor='hand2', text='Log in', bg='green', fg='yellow', font='Arial',
                                  command=Login_Page_from_SignUp_page)
Login_Redirect_Button.grid(row=10, column=0, pady=10)

# ---------------------------------------#LOGIN*PAGE*CONTENT#-------------------------------------------------#

# Content for the Login Page
login_label = tk.Label(login_frame, text='Login', font=('Arial', 20), fg='firebrick1')
login_label.grid(row=0, column=0, columnspan=2, pady=10)

username_label = tk.Label(login_frame, text='Username:', font='Arial')
username_label.grid(row=1, column=0, padx=10, pady=5, sticky='w')

First_name_entry_2 = tk.Entry(login_frame, bd=0, bg='white')
First_name_entry_2.grid(row=1, column=1, padx=10, pady=5)

password_label = tk.Label(login_frame, text='Password:', font='Arial')
password_label.grid(row=2, column=0, padx=10, pady=5, sticky='w')

pass_entry = tk.Entry(login_frame, show='*', bd=0, bg='white')  # Mask the password
pass_entry.grid(row=2, column=1, padx=10, pady=5)

forget_button = tk.Button(login_frame, text='Forget password?', bd=0, activebackground='white', bg='white',
                          cursor='hand2', fg='firebrick1', font='Arial', command=Forget_Button)
forget_button.grid(row=4, column=0, columnspan=2, pady=10)

or_label = tk.Label(login_frame, text='----------------OR---------------------', fg='purple', font='Arial')
or_label.grid(row=5, column=0, columnspan=2, pady=10)

Login_google = tk.Button(login_frame, text='G+', font='Arial', fg='white', cursor='hand2', bg='firebrick1',
                         activeforeground='white')
Login_google.grid(row=6, column=0, columnspan=2, pady=10)

login_button = tk.Button(login_frame, text='Login', bg='green', fg='yellow', font='Arial', cursor='hand2',
                         command=Connect_DB)
login_button.grid(row=3, column=0, columnspan=2, pady=10)

signup_label = tk.Label(login_frame, text='Dont have an account?', fg='firebrick1', font='Arial')
signup_label.grid(row=7, column=0, columnspan=2, pady=10)

Create_new_account = tk.Button(login_frame, text='CreateOne', bg='green', fg='yellow', font='Arial', cursor='hand2',
                               command=SignUp_page_to_Login_Page)
Create_new_account.grid(row=8, column=0, columnspan=2, pady=10)

# ---------------------------#HOME*PAGE*CONTENT#--------------------------------------------#


# Create the content for the Home page
msg = tk.Label(home_frame, text='ONLINE VOTING PLATFORM', font=('dubai', 24), bg='lightblue')
msg.pack(fill='x')

greetings = tk.Label(home_frame,
                     text='HELLO VOTERS! WELCOME TO THE SECURED VOTING PLATFORM VOTE ME',
                     height=5, font=('Fantasy', 20), fg='blue')
greetings.pack()

# --------------------------------------#VOTEME*PAGE*CONTENT#------------------------------------------------#

# Create the content for the VoteMe page
first_name_label_1 = tk.Label(voteme_frame, text='First Name:', font='Arial')
first_name_label_1.grid(row=0, column=0, padx=10, pady=5, sticky='w')

first_name_entry_1 = tk.Entry(voteme_frame)
first_name_entry_1.grid(row=0, column=1, padx=10, pady=5)

last_name_label_1 = tk.Label(voteme_frame, text='Last Name:', font='Arial')
last_name_label_1.grid(row=1, column=0, padx=10, pady=5, sticky='w')

last_name_entry_1 = tk.Entry(voteme_frame)
last_name_entry_1.grid(row=1, column=1, padx=10, pady=5)

dob_label = tk.Label(voteme_frame, text='Date of Birth:', font='Arial')
dob_label.grid(row=2, column=0, padx=10, pady=5, sticky='w')

dob_entry = tk.Entry(voteme_frame)
dob_entry.grid(row=2, column=1, padx=10, pady=5)

aadhar_label = tk.Label(voteme_frame, text='Aadhar Number:', font='Arial')
aadhar_label.grid(row=3, column=0, padx=10, pady=5, sticky='w')

aadhar_entry = tk.Entry(voteme_frame)
aadhar_entry.grid(row=3, column=1, padx=10, pady=5)

selectParty = tk.Label(voteme_frame, text='Select To Vote:', font='Arial')
selectParty.grid(row=4, column=0, padx=10, pady=5, sticky='w')

selectParty_entry = tk.Entry(voteme_frame)
selectParty_entry.grid(row=4, column=1, padx=10, pady=5)

submit_button = tk.Button(voteme_frame, text='Submit', bg='green', fg='yellow', font='Arial', command=Vote_ME_DB)
submit_button.grid(row=6, column=0, columnspan=2, pady=10)

# -------------------------------------#HOME*PAGE*CONTENT+SWITCH*PAGE*LOGIC#----------------------------------#
# Hide all pages initially except the Home page
for page in pages[1:]:
    page.pack_forget()

# Pack the Home page to start
home_frame.pack(fill='both', expand=True)

# Create a label for the voting instructions (you can add this to any page)
voting_instructions_text = """
**Voting Instructions**

1. **Account Creation**: - If you already have a VoteMe account, log in using your username and password. - If you 
are a new user, click on the "Sign Up" button to create an account. Provide accurate information and follow the 
registration process.

2. **Verification (if applicable)**: - Depending on the election or organization's requirements, you may be asked to 
verify your identity. Follow the provided instructions for identity verification.

3. **Access the Ballot**:
   - Once logged in, you will be directed to the ballot page.
   - Review the candidates or options available for the election.

4. **Candidate Information**: - Click on the candidate's name or option to access additional information such as 
their platform, qualifications, and other relevant details.

5. **Make Your Selection**:
   - To vote for a candidate or option, click the corresponding button or checkbox next to their name.
   - Ensure that your selection is accurately reflected before proceeding.

6. **Review Your Vote**:
   - Before submitting your vote, take a moment to review your selections.
   - Verify that you have chosen the candidates or options you intend to vote for.

7. **Submit Your Vote**:
   - When you are satisfied with your selections, click the "Cast Vote" or "Submit" button to finalize your vote.
   - Some elections may require an additional confirmation step.

8. **Confirmation**:
   - After successfully casting your vote, you will receive a confirmation message or notification.
   - Note any confirmation numbers or receipts provided for your records.

9. **Logout (if applicable)**: - If you are using a shared or public computer, ensure that you log out of your 
account to protect your privacy and security.

10. **Contact Support**: - If you encounter any issues, have questions, or need assistance during the voting process, 
do not hesitate to contact our dedicated support team.

11. **Keep Voting Information Secure**: - Safeguard your login credentials, confirmation numbers, or receipts. These 
may be required for auditing or dispute resolution.

12. **Respect Deadlines**:
   - Be aware of the voting deadlines and cast your vote within the specified timeframe. Late votes may not be counted.

13. **Stay Informed**: - Stay informed about the election process, including important dates, candidates' profiles, 
and any updates or announcements from the election organizers.

Thank you for participating in the democratic process through VoteMe. Your vote plays a crucial role in shaping the 
future, and we are committed to ensuring a fair and reliable voting experience for all users. Happy Voting!"""

# Create a Text widget with scrollbar for voting instructions
voting_instructions_text_widget = tk.Text(home_frame, wrap=tk.WORD, bg='lightcyan', font=('Arial', 12))
voting_instructions_text_widget.pack(fill='both', expand=True)

# Create a scrollbar and connect it to the Text widget
scrollbar = tk.Scrollbar(voting_instructions_text_widget, command=voting_instructions_text_widget.yview)
scrollbar.pack(side='right', fill='y')
voting_instructions_text_widget.config(yscrollcommand=scrollbar.set)

# Insert the voting instructions text into the Text widget
voting_instructions_text_widget.insert('1.0', voting_instructions_text)

# Content for the About Us Page
# Create a Text widget for the "About Us" page
about_us_text_widget = tk.Text(about_us_frame, wrap=tk.WORD, bg='lightcyan', font=('Arial', 12))
about_us_text_widget.pack(fill='both', expand=True)

# Create a scrollbar and connect it to the Text widget
scrollbar_about_us = tk.Scrollbar(about_us_text_widget, command=about_us_text_widget.yview)
scrollbar_about_us.pack(side='right', fill='y')
about_us_text_widget.config(yscrollcommand=scrollbar_about_us.set)

# Add the "About Us" content to the Text widget
about_us_content = """
Welcome to VoteMe, your trusted online voting platform. Our mission is to provide a secure and convenient way for individuals to participate in the democratic process. We're committed to ensuring that every vote counts and that the voting experience is accessible to all.

Who We Are

VoteMe was founded by a team of dedicated individuals with a passion for democracy and technology. Our diverse backgrounds in software development, cybersecurity, and political science have allowed us to create a voting platform that combines innovation with the highest standards of security and integrity.

Our Vision

Our vision is to revolutionize the way people vote. We believe in a future where voting is not only easy and efficient but also highly secure. Through cutting-edge technology, we aim to build a bridge between citizens and their right to vote, making the process smoother, more transparent, and more inclusive.

Why Choose VoteMe?

Security: Your trust and security are our top priorities. We employ robust security measures to protect your personal information and ensure that your vote remains confidential.

Accessibility: VoteMe is designed to be user-friendly and accessible to all. We believe in equal voting opportunities for every citizen, regardless of their background or abilities.

Transparency: We are committed to providing complete transparency in the voting process. You can trust that your vote will be accurately counted.

Innovation: We continuously innovate to keep up with the ever-changing technological landscape. Our platform is at the forefront of the industry, providing a seamless voting experience.

Support: Our dedicated support team is here to assist you with any questions or issues you may have. We're just a message away.

Get Involved

Join us in shaping the future of online voting. Your participation is crucial, and your voice matters. Together, we can make the democratic process more accessible and secure than ever before.

Thank you for choosing VoteMe as your online voting platform. We look forward to serving you in your voting journey.

If you have any questions, feedback, or suggestions, please don't hesitate to reach out to us. We're here to help!
"""

# Insert the "About Us" content into the Text widget
about_us_text_widget.insert('1.0', about_us_content)

# Content for the Contact Us Page
# Content for the Contact Us Page
contact_us_label = tk.Label(contact_Us, text='Contact Us', font=('Arial', 20), fg='firebrick1')
contact_us_label.grid(row=0, column=0, columnspan=2, pady=10)

contact_us_content = tk.Label(contact_Us,
                              text='For any inquiries or assistance, please feel free to contact our support team.\n'
                                   'We are here to help you with any questions or issues you may have.\n'
                                   'You can reach us through the following contact information:\n\n'
                                   'Email: support@voteme.com\n'
                                   'Phone: +1 (123) 456-7890\n'
                                   'Address: 1234 Main Street, Your City, Your Country\n\n'
                                   'Our dedicated team is available during business hours to assist you. Your '
                                   'feedback and inquiries are important to us!',
                              font=('Arial', 14), fg='blue')
contact_us_content.grid(row=1, column=0, columnspan=2, pady=10)

root.mainloop()
