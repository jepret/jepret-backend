from flask import g, request
from core.middleware import Middleware
from core.error import BaseError
from redis_model import Session


class AuthMiddleware(Middleware):
    def default(self):
        raise BaseError("Unauthorized", 401)

    def check(self, *args, **kwargs):
        token = request.headers.get('Authorization', None)
        if not token:
            return False

        session = Session(token)
        g.user = session.load()
        return g.user is not None
