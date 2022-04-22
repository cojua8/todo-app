class UserNotFoundException(Exception):
    def __init__(self, username):
        self.username = username

    def __str__(self):
        return f"Could not find user: {self.username}."
