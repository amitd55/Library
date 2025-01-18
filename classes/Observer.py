class Observer:
    def __init__(self, username):
        """Initialize an observer with a username."""
        self.username = username

    def update(self, message):
        """Receive and handle a notification."""
        print(f"Notification for {self.username}: {message}")
