from tkinter import messagebox
import customtkinter as ctk
from functions.g_pass import GPass
from functions.sh import Password
import sqlite3
import datetime
import re

class AddFrame(ctk.CTkFrame):
    def __init__(self, master, return_to_menu):
        self.return_to_menu = return_to_menu
        self.g_pass = GPass()
        self.conn = sqlite3.connect('name_of_db.db')
        self.c = self.conn.cursor()
        super().__init__(master)

        self.acct_label = ctk.CTkLabel(self, text="Account Name:")
        self.acct_label.pack()

        self.acct_entry = ctk.CTkEntry(self)
        self.acct_entry.pack()

        self.email_label = ctk.CTkLabel(self, text="Email:")
        self.email_label.pack()

        self.email_entry = ctk.CTkEntry(self)
        self.email_entry.pack()

        self.existing_code_var = ctk.BooleanVar()
        self.existing_code_var.set(False)

        self.existing_code_check = ctk.CTkCheckBox(self, text="Already have a code?", variable=self.existing_code_var, command=self.toggle_custom_code_entry)
        self.existing_code_check.pack()

        self.code_label = ctk.CTkLabel(self, text="Existing code:")
        self.code_label.pack()

        self.code_entry = ctk.CTkEntry(self, show="*")
        self.code_entry.pack()

        self.submit_button = ctk.CTkButton(self, text="Submit", command=self.save_and_return)
        self.submit_button.pack()

        self.cancel_button = ctk.CTkButton(self, text="Cancel", command=self.cancel_and_return)
        self.cancel_button.pack()

        self.code_label.pack_forget()
        self.code_entry.pack_forget()

        master.bind("<Return>", self.save_and_return)


    def toggle_custom_code_entry(self):
        if self.existing_code_var.get():
            self.code_label.pack()
            self.code_entry.pack()
        else:
            self.code_label.pack_forget()
            self.code_entry.pack_forget()
    
    def save_and_return(self, event=None):
        acct = self.acct_entry.get()
        email = self.email_entry.get()

        if not self.validate_input(acct, email):
            messagebox.showerror("Error", "Invalid input.")
            return

        if self.existing_code_var.get() and self.code_entry.get():
            pw = self.generate_password(self.code_entry.get())
        else:
            pw = self.generate_password()
            self.code_entry.insert(0, pw)

        if self.save_password(acct, email, pw):
            messagebox.showinfo("Success", "Password saved successfully.")
            self.destroy()
            if self.return_to_menu:
                self.return_to_menu()
        else:
            messagebox.showerror("Error", "Failed to save password.")

    def generate_password(self, code=None):
        if code is None:
            code = self.g_pass.generate_random_string()
        return self.g_pass.g_pass(code)
    
    def save_password(self, acct, email, pw):
        try:
            update_timestamp = datetime.datetime.now()
            p = Password(acct, email, pw, update_timestamp)
            self.c.execute("INSERT INTO passwords (acct, email, p, update_timestamp) VALUES (?, ?, ?, ?)", (p.acct, self.g_pass.encrypt(p.email), self.g_pass.encrypt(p.p), p.update_timestamp))
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False
        
    def cancel_and_return(self):
        self.destroy()
        if self.return_to_menu:
            self.return_to_menu()    
            
    def validate_input(self, acct, email):
        acct_valid = re.match(r'^[a-zA-Z0-9_-]{3,50}$', acct)  # Account name should be alphanumeric, 3-50 characters
        email_valid = re.match(r'^[^@]+@[^@]+\.[^@]+$', email)  # Simple email validation
        return acct_valid and email_valid


    
