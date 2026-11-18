class InvalidPasswordError(Exception):
    def __init__(self):
        self.message = "The password is invalid"
        self.status = 400
        super().__init__(self.message)