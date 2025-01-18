class Logger:
    def __init__(self, log_file="library_logs.txt"):
        self.log_file = log_file

    def log_action(self, func):
        def wrapper(*args, **kwargs):
            try:
                # Call the original function and get the result
                result = func(*args, **kwargs)
                action_name = func.__name__

                # Map custom actions to log messages
                log_messages = {
                    "add_book": "book added",
                    "remove_book": "book removed",
                    "perform_search": "Search book",
                    "borrow_book": "book borrowed",
                    "return_book": "book returned",
                    "log_out": "log out",
                    "log_in": "logged in",
                    "register": "registered",
                    "display_popular_books": "Popular books display",
                }

                # Default action log message
                action = log_messages.get(action_name, action_name.replace('_', ' ').title())
                status = "successfully" if result else "fail"

                # Special case for search action
                if action_name == "perform_search":
                    query = args[1]
                    search_type = args[2]
                    search_type_log = "name" if search_type == "title" else search_type
                    log_message = f"{action} \"{query}\" by {search_type_log} completed {status}\n"
                else:
                    log_message = f"{action} {status}\n"

                # Write the log message to the log file
                with open(self.log_file, "a") as log_file:
                    log_file.write(log_message)

                return result
            except Exception as e:
                action = func.__name__.replace('_', ' ').title()
                log_message = f"{action} failed: {str(e)}\n"
                with open(self.log_file, "a") as log_file:
                    log_file.write(log_message)
                raise
        return wrapper
