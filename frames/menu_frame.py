from tkinter import messagebox
import csv 
from tkinter import filedialog as fd
import customtkinter as ctk
from functions.g_pass import GPass
from frames.view_frame import ViewFrame
from frames.add_frame import AddFrame
from frames.update_frame import UpdateFrame
from frames.delete_frame import DeleteFrame
import sqlite3

conn = sqlite3.connect('name_of_db.db')
c = conn.cursor()

# Create passwords table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS passwords (acct text, email text, p text, update_timestamp text)''')

# Check for phrases table existence and create if not exist
c.execute('''CREATE TABLE IF NOT EXISTS phrases (id INTEGER PRIMARY KEY AUTOINCREMENT, phrase text)''')

# Check for pins table existence and create if not exist
c.execute('''CREATE TABLE IF NOT EXISTS pins (id INTEGER PRIMARY KEY AUTOINCREMENT, pin text)''')

conn.commit()
conn.close()

class MenuFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.conn = sqlite3.connect('testing.db')
        self.c = self.conn.cursor()
        self._appearance = ctk.set_appearance_mode("dark")
        self._color = ctk.set_default_color_theme("blue")
        self.g_pass = GPass()

        self.crud_label = ctk.CTkLabel(self, text="C, R, U, D, add files, exit: (1/2/3/4/5/6)")
        self.crud_label.pack()

        self.crud_entry = ctk.CTkEntry(self)
        self.crud_entry.pack()

        self.crud_button = ctk.CTkButton(self, text="Submit", command=self.process_input)
        self.crud_button.pack()

        master.bind("<Return>", self.process_input)

    def process_input(self, event=None):
        choice = self.crud_entry.get()
        if choice == "1":
            self.add_password()
        elif choice == "2":
            self.view_passwords()
        elif choice == "3":
            self.update_password()
        elif choice == "4":
            self.delete_password()
        elif choice == "5":
            self.add_files()
        elif choice == "6":
            self.master.destroy()
        else:
            messagebox.showerror("Invalid Input", "Please enter a valid choice (1/2/3/4/5/6)")
        
    def add_password(self):
        self.destroy()
        self.add_frame = AddFrame(self.master, self.return_to_menu)
        self.add_frame.pack()

    def view_passwords(self):
        self.destroy()
        passwords = self.retrieve_passwords()
        if passwords:
            self.view_frame = ViewFrame(self.master, passwords, return_to_menu=self.return_to_menu)
            self.view_frame.pack()
        else:
            messagebox.showinfo("No Accounts", "No accounts found.")
    
    def update_password(self):
        self.destroy()
        self.update_frame = UpdateFrame(self.master, self.return_to_menu)
        self.update_frame.pack()
    
    def delete_password(self):
        self.destroy()
        self.delete_frame = DeleteFrame(self.master, self.return_to_menu)
        self.delete_frame.pack()

    def retrieve_passwords(self):
        try:
            accounts = self.c.execute("SELECT acct, email, p, update_timestamp FROM passwords").fetchall()
            return accounts
        except Exception as e:
            print(e)
            return None
        
    def add_files(self):
        try:
            phrases_path = fd.askopenfilename(title="Select CSV File For Phrases", filetypes=[("CSV Files", "*.csv")])
            if not phrases_path:
                return

            with open(phrases_path, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    encrypted_phrase = self.g_pass.encrypt(row[0])
                    self.c.execute("INSERT INTO phrases (phrase) VALUES (?)", (encrypted_phrase,))

            pins_path = fd.askopenfilename(title="Select CSV File For Pins", filetypes=[("CSV Files", "*.csv")])
            if not pins_path:
                return
            with open(pins_path, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    encrypted_pin = self.g_pass.encrypt(row[0])
                    self.c.execute("INSERT INTO pins (pin) VALUES (?)", (encrypted_pin,))
            self.conn.commit()
            self.conn.close()
            self.return_to_menu()
        except Exception as e:
            print(e)
            messagebox.showerror("Error", "An error occurred while adding phrases.")
    
    def return_to_menu(self):
        self.destroy()
        new_menu_frame = MenuFrame(self.master)
        new_menu_frame.pack()