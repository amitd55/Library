import os
import pandas as pd

class FileHandler:
    def __init__(self, base_dir="data"):
        self.base_dir = os.path.abspath(base_dir)
        if not os.path.exists(self.base_dir):
            print(f"Warning: The directory {self.base_dir} does not exist.")
        else:
            os.makedirs(self.base_dir, exist_ok=True)

    def get_file_path(self, file_name):
        return os.path.join(self.base_dir, file_name)

    def load_csv(self, file_name):
        file_path = self.get_file_path(file_name)
        try:
            if os.path.exists(file_path):
                return pd.read_csv(file_path)
            else:
                print(f"File {file_name} does not exist. Returning an empty DataFrame.")
                return pd.DataFrame()
        except Exception as e:
            print(f"Error loading {file_name}: {e}")
            return pd.DataFrame()

    def save_csv(self, file_name, data):
        file_path = self.get_file_path(file_name)
        try:
            data.to_csv(file_path, index=False)
        except Exception as e:
            print(f"Error saving {file_name}: {e}")

    def update_file(self, file_name, new_data):
        file_path = self.get_file_path(file_name)
        try:
            existing_data = self.load_csv(file_name)
            if not existing_data.empty:
                updated_data = pd.concat([existing_data, new_data]).drop_duplicates(ignore_index=True)
            else:
                updated_data = new_data
            self.save_csv(file_name, updated_data)
        except Exception as e:
            print(f"Error updating file {file_name}: {e}")
