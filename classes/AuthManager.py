import pandas as pd
import hashlib
from classes.FileHandler import FileHandler
from classes.Logger import Logger


class AuthManager:
    def __init__(self, user_file="users.csv"):
        self.file_handler = FileHandler()
        self.user_file = user_file
        self.initialize_default_user()

    def hash_password(self, password):
        """Hash a password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()

    def initialize_default_user(self):
        """Ensure a default admin user exists."""
        users = self.load_users()

        if users.empty:
            default_user = pd.DataFrame([{
                "username": "admin",
                "password_hash": self.hash_password("admin123"),
            }])
            self.save_users(default_user)
            print("Default admin user created: Username: 'admin', Password: 'admin123'")
        else:
            print("Users already exist. No default admin user added.")

    def load_users(self):
        """Load users from the CSV file using FileHandler."""
        try:
            users_data = self.file_handler.load_csv(self.user_file)
            if users_data.empty:
                print(f"{self.user_file} exists but contains no data. Returning an empty DataFrame.")
                return pd.DataFrame(columns=["username", "password_hash"])  # Empty DataFrame
            print(f"Loaded {len(users_data)} users from {self.user_file}.")
            return users_data
        except FileNotFoundError:
            print(f"{self.user_file} not found. Initializing empty user DataFrame.")
            return pd.DataFrame(columns=["username", "password_hash"])  # Empty DataFrame
        except Exception as e:
            print(f"Error loading users: {e}")
            return pd.DataFrame(columns=["username", "password_hash"])  # Empty DataFrame

    def save_users(self, users_df):
        """Save the DataFrame of users back to the CSV file."""
        try:
            self.file_handler.save_csv(self.user_file, users_df)
            print(f"Users saved successfully to {self.user_file}.")
        except Exception as e:
            print(f"Error saving users: {e}")

    @Logger().log_action
    def register(self, username, password):
        """Register a new user."""
        users = self.load_users()  # Load existing users

        # Check if the username already exists
        if username in users["username"].values:
            return "Registration failed: Username already exists."

        # Add the new user
        new_user = pd.DataFrame([{
            "username": username,
            "password_hash": self.hash_password(password),
        }])
        updated_users = pd.concat([users, new_user], ignore_index=True)
        print(f"Updated users: {updated_users}")

        # Save the updated DataFrame
        self.save_users(updated_users)

        return "Registration successful."

    @Logger().log_action
    def login(self, username, password):
        """Log in an existing user."""
        users = self.load_users()

        if username in users["username"].values:
            hashed_password = self.hash_password(password)
            stored_password = users.loc[users["username"] == username, "password_hash"].iloc[0]
            if hashed_password == stored_password:
                return "Login successful."

        return "Login failed: Invalid username or password."
