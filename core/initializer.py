import os
from typing import List
from flask import Flask
from flask_admin import Admin

from core.error_handler import base_error_handler
from core.router import Router


def initialize(name, routers: List[Router], admin_views: List):
    app = Flask(name)
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    admin = Admin(app)
    for v in admin_views:
        admin.add_view(v)

    app.register_error_handler(500, base_error_handler)
    for r in routers:
        r.register(app)

    return app
