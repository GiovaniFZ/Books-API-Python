class UserNotFoundError(Exception):
    def __init__(self):
        self.message = "User not found"
        self.status = 404
        super().__init__(self.message)