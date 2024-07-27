import customtkinter as ctk
from functions.g_pass import GPass

class ViewFrame(ctk.CTkFrame):
    def __init__(self, master, passwords, return_to_menu):
        super().__init__(master)
        self.return_to_menu = return_to_menu
        self.g_pass = GPass()
        self.passwords_label = ctk.CTkLabel(self, text="Passwords:")
        self.passwords_label.pack()

        # Create a list to hold the Checkbuttons
        self.checkboxes = []

        for password in enumerate(passwords):
            password_info = f"Account: {password[0]}, Email: {self.g_pass.decrypt(password[1])}, Password: {self.g_pass.decrypt(password[2])}, Date: {password[3]}"
            password_label = ctk.CTkLabel(self, text=password_info)
            password_text = ctk.CTkEntry(self, state="normal")
            password_text.insert(0, self.g_pass.decrypt(password[2]))
            password_label.pack()
            password_text.pack()


        # Add a button to return to the menu
        self.return_button = ctk.CTkButton(self, text="Return to Menu", command=self.return_to_menu_and_destroy)
        self.return_button.pack()

        master.bind("<Return>", self.return_to_menu_and_destroy)

    def return_to_menu_and_destroy(self, event=None):
        # Call the return_to_menu function
        self.return_to_menu()
        # Destroy the ViewFrame instance
        self.destroy()


