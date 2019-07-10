from cerberus.validator import Validator
from flask import request

from core.middleware import Middleware
from core.error import BaseError


class BaseValidator(Middleware):
    def __init__(self, schema):
        Middleware.__init__(self)
        self.next = None
        self.validator = Validator()
        self.schema = schema

    def check(self):
        return self.validator.validate(request.json, self.schema)

    def default(self):
        raise BaseError(message=self.validator.errors, status_code=400)
