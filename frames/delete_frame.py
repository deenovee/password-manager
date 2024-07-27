from tkinter import messagebox
import customtkinter as ctk
import sqlite3
import re

class DeleteFrame(ctk.CTkFrame):
    def __init__(self, master, return_to_menu):
        self.conn = sqlite3.connect('name_of_db.db')
        self.c = self.conn.cursor()
        super().__init__(master)
        self.return_to_menu = return_to_menu  # Save return_to_menu function

        self.acct_label = ctk.CTkLabel(self, text="Account Name:")
        self.acct_label.pack()

        self.acct_entry = ctk.CTkEntry(self)
        self.acct_entry.pack()

        self.delete_button = ctk.CTkButton(self, text="Delete", command=self.delete)
        self.delete_button.pack()

        self.cancel_button = ctk.CTkButton(self, text="Cancel", command=self.cancel_and_return)
        self.cancel_button.pack()

        master.bind("<Return>", self.delete)

    def validate_input(self, acct):
        acct_valid = re.match(r'^[a-zA-Z0-9_-]{3,50}$', acct)  # Account name should be alphanumeric, 3-50 characters
        return acct_valid is not None

    def delete(self, event=None):
        acct = self.acct_entry.get()

        if not self.validate_input(acct):
            messagebox.showerror("Error", "Invalid account name.")
            return

        if self.delete_password(acct):
            messagebox.showinfo("Success", "Account Deleted Successfully")
            self.destroy()
            # Call the return_to_menu function to return to the menu
            self.return_to_menu()
        else:
            messagebox.showerror("Error", "Failed to delete password.")

    def delete_password(self, acct):
        try:
            self.c.execute("DELETE FROM passwords WHERE acct = ?", (acct,))
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False
        
    def cancel_and_return(self):    
        self.destroy()
        if self.return_to_menu:
            self.return_to_menu()
