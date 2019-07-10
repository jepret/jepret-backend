from core.util import respond_data
from flask import request


def test_post():
    return respond_data({"name": request.json["name"]})


def test_get(name):
    return respond_data({"name": name})
