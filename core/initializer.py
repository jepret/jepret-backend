from typing import List
from flask import Flask

from core.error_handler import base_error_handler
from core.router import Router


def initialize(name, routers: List[Router]):
    app = Flask(name)
    app.register_error_handler(500, base_error_handler)
    for r in routers:
        r.register(app)

    return app
