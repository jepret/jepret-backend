class BaseError(Exception):
    def __init__(self, message, status_code=500):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code

    def to_dict(self):
        return {"code": self.status_code, "message": self.message}
