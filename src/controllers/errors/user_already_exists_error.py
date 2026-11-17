class UserAlreadyExistsError(Exception):
    def __init__(self):
        self.message = "User already exists"
        self.status = 409
        super().__init__(self.message)