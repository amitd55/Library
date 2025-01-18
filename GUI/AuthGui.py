import tkinter as tk
from tkinter import messagebox
from classes.AuthManager import AuthManager

class AuthGui:
    def __init__(self, on_success):
        self.auth_manager = AuthManager()
        self.on_success = on_success  # Callback for successful login or registration
        self.root = tk.Tk()  # Main application root
        self.root.title("Authentication")
        self.root.geometry("400x300")

    def build_gui(self, action):
        tk.Label(self.root, text=f"{action.capitalize()} Screen", font=("Arial", 16)).pack(pady=20)

        tk.Label(self.root, text="Username").pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        tk.Label(self.root, text="Password").pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()

        if action == "login":
            tk.Button(self.root, text="Login", command=self.login).pack(pady=10)
            tk.Button(self.root, text="Go to Register", command=lambda: self.switch_to("register")).pack(pady=10)
        elif action == "register":
            tk.Button(self.root, text="Register", command=self.register).pack(pady=10)
            tk.Button(self.root, text="Go to Login", command=lambda: self.switch_to("login")).pack(pady=10)

    def switch_to(self, action):
        """Switch between login and register screens."""
        self.root.destroy()  # Properly destroy the current window
        app = AuthGui(on_success=self.on_success)
        app.run(action)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "All fields are required.")
            return

        result = self.auth_manager.login(username, password)
        if "successful" in result:
            messagebox.showinfo("Login", result)
            self.root.destroy()  # Close the login window after successful login
            self.on_success(username)  # Pass the logged-in user to the callback
        else:
            messagebox.showerror("Login Failed", result)

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "All fields are required.")
            return

        # Call register without logged_in_user
        result = self.auth_manager.register(username, password)
        if "successful" in result:
            messagebox.showinfo("Register", result)
            self.root.destroy()  # Close the register window after successful registration
            self.on_success(username)  # Pass the registered user to the callback
        else:
            messagebox.showerror("Registration Failed", result)

    def run(self, action):
        self.build_gui(action)
        self.root.mainloop()

