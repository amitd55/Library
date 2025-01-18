import unittest
from classes.WaitingListManager import WaitingListManager


class TestWaitingListManager(unittest.TestCase):
    def setUp(self):
        self.waiting_list_manager = WaitingListManager()

    def test_add_to_waiting_list(self):
        self.waiting_list_manager.add_to_waiting_list("user1")
        self.assertIn("user1", self.waiting_list_manager.get_waiting_list())

        self.waiting_list_manager.add_to_waiting_list("user2")
        self.assertIn("user2", self.waiting_list_manager.get_waiting_list())

        # Ensure duplicates are not added
        self.waiting_list_manager.add_to_waiting_list("user1")
        self.assertEqual(self.waiting_list_manager.get_waiting_list().count("user1"), 1)

    def test_remove_from_waiting_list(self):
        self.waiting_list_manager.add_to_waiting_list("user1")
        self.waiting_list_manager.add_to_waiting_list("user2")

        removed_user = self.waiting_list_manager.remove_from_waiting_list()
        self.assertEqual(removed_user, "user1")
        self.assertNotIn("user1", self.waiting_list_manager.get_waiting_list())

        removed_user = self.waiting_list_manager.remove_from_waiting_list()
        self.assertEqual(removed_user, "user2")
        self.assertNotIn("user2", self.waiting_list_manager.get_waiting_list())

        # Ensure removing from an empty list returns None
        removed_user = self.waiting_list_manager.remove_from_waiting_list()
        self.assertIsNone(removed_user)

    def test_clear_waiting_list(self):
        self.waiting_list_manager.add_to_waiting_list("user1")
        self.waiting_list_manager.add_to_waiting_list("user2")

        self.waiting_list_manager.clear_waiting_list()
        self.assertEqual(len(self.waiting_list_manager.get_waiting_list()), 0)

    def test_observer_integration(self):
        self.waiting_list_manager.add_to_waiting_list("user1")
        self.waiting_list_manager.add_to_waiting_list("user2")

        # Check if observers are added for each user
        self.assertEqual(len(self.waiting_list_manager.observers), 2)

        # Remove a user and ensure observer is removed
        self.waiting_list_manager.remove_from_waiting_list()
        self.assertEqual(len(self.waiting_list_manager.observers), 1)

        # Clear all observers
        self.waiting_list_manager.clear_waiting_list()
        self.assertEqual(len(self.waiting_list_manager.observers), 0)

    def test_notify_observers(self):
        self.waiting_list_manager.add_to_waiting_list("user1")
        self.waiting_list_manager.add_to_waiting_list("user2")

        # Mock observers to capture messages
        class MockObserver:
            def __init__(self, username):
                self.username = username
                self.messages = []

            def update(self, message):
                self.messages.append(message)

        mock_observer1 = MockObserver("user1")
        mock_observer2 = MockObserver("user2")

        self.waiting_list_manager.observers = [mock_observer1, mock_observer2]

        self.waiting_list_manager.notify_observers("Test Message")

        self.assertIn("Test Message", mock_observer1.messages)
        self.assertIn("Test Message", mock_observer2.messages)


if __name__ == "__main__":
    unittest.main()
