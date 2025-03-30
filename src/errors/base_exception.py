class MyException(Exception):
    message = "Something went wrong"

    def __init__(self, message=None, **details):
        if message:
            self.message = message
        super().__init__(self.message)
        self.details = details

    def __str__(self):
        if self.details:
            return f"{self.message}, details={self.details}"
        return f"{self.message}"
