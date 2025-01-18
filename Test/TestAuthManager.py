import unittest
import os
import pandas as pd
from unittest.mock import patch, MagicMock
from classes.AuthManager import AuthManager  # Replace with the actual file name containing your AuthManager class

class TestAuthManager(unittest.TestCase):

    def setUp(self):
        self.mock_file_handler = MagicMock()
        self.mock_logger = MagicMock()
        self.auth_manager = AuthManager(user_file="test_users.csv")
        self.auth_manager.file_handler = self.mock_file_handler
        self.patcher = patch('classes.Logger.Logger.log_action', lambda x: x)
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()
        if os.path.exists("test_users.csv"):
            os.remove("test_users.csv")

    def test_initialize_default_user(self):
        # Test if the default admin user is created
        self.mock_file_handler.load_csv.side_effect = FileNotFoundError()
        self.mock_file_handler.save_csv = MagicMock()
        self.auth_manager.initialize_default_user()

        self.mock_file_handler.save_csv.assert_called_once()
        saved_data = self.mock_file_handler.save_csv.call_args[0][1]

        self.assertEqual(len(saved_data), 1)
        self.assertEqual(saved_data.iloc[0]['username'], 'admin')

    def test_register_new_user(self):
        # Mock initial users file
        self.mock_file_handler.load_csv.return_value = pd.DataFrame(columns=["username", "password_hash"])
        self.mock_file_handler.save_csv = MagicMock()
        response = self.auth_manager.register("test_user", "test_password")

        self.assertEqual(response, "Registration successful.")
        self.mock_file_handler.save_csv.assert_called_once()
        saved_data = self.mock_file_handler.save_csv.call_args[0][1]
        self.assertTrue("test_user" in saved_data["username"].values)

    def test_register_existing_user(self):
        # Mock users file with an existing user
        self.mock_file_handler.load_csv.return_value = pd.DataFrame({
            "username": ["test_user"],
            "password_hash": [self.auth_manager.hash_password("test_password")]
        })

        response = self.auth_manager.register("test_user", "new_password")

        self.assertEqual(response, "Registration failed: Username already exists.")

    def test_login_successful(self):
        # Mock users file with an existing user
        self.mock_file_handler.load_csv.return_value = pd.DataFrame({
            "username": ["test_user"],
            "password_hash": [self.auth_manager.hash_password("test_password")]
        })

        response = self.auth_manager.login("test_user", "test_password")

        self.assertEqual(response, "Login successful.")

    def test_login_failed(self):
        # Mock users file with an existing user
        self.mock_file_handler.load_csv.return_value = pd.DataFrame({
            "username": ["test_user"],
            "password_hash": [self.auth_manager.hash_password("test_password")]
        })

        # Incorrect username
        response = self.auth_manager.login("wrong_user", "test_password")
        self.assertEqual(response, "Login failed: Invalid username or password.")

        # Incorrect password
        response = self.auth_manager.login("test_user", "wrong_password")
        self.assertEqual(response, "Login failed: Invalid username or password.")

if __name__ == "__main__":
    unittest.main()
