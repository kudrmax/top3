class MyException(Exception):
    message = "Something went wrong"

    def __init__(self, **details):
        super().__init__(self.message)
        self.details = details

    def __str__(self):
        if self.details:
            return f"{self.message}, details={self.details}"
        return f"{self.message}"
