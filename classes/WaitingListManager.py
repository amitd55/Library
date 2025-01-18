from classes.Observer import Observer


class WaitingListManager:
    def __init__(self):
        self.waiting_list = ""  # Comma-separated string for client names
        self.observers = []  # List of observer instances

    def add_to_waiting_list(self, username):
        """Add a user to the waiting list and register an observer."""
        if username not in self.get_waiting_list():
            if self.waiting_list:
                self.waiting_list += f",{username}"
            else:
                self.waiting_list = username
            self.add_observer(Observer(username))

    def remove_from_waiting_list(self):
        """Remove the first user in the waiting list and notify them."""
        current_list = self.get_waiting_list()
        if current_list:
            username = current_list.pop(0)
            self.waiting_list = ",".join(current_list)
            self.notify_observers(f"The book is now available for {username}.")
            self.remove_observer_by_username(username)
            return username
        return None

    def clear_waiting_list(self):
        """Clear the waiting list and remove all observers."""
        self.waiting_list = ""
        self.observers.clear()

    def get_waiting_list(self):
        """Retrieve the waiting list as a list."""
        return self.waiting_list.split(",") if self.waiting_list else []

    # Observer Management
    def add_observer(self, observer):
        """Add an observer to the list."""
        self.observers.append(observer)

    def remove_observer_by_username(self, username):
        """Remove an observer based on the username."""
        self.observers = [obs for obs in self.observers if obs.username != username]

    def notify_observers(self, message):
        """Notify all observers with the given message."""
        for observer in self.observers:
            observer.update(message)

