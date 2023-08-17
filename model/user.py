class User:

    def __init__(self, username: str):
        self.username = username

    def __dict__(self):
        return {
            "username": self.username
        }