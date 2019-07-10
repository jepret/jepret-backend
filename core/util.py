from string import ascii_letters
from flask import jsonify
from random import choice


def respond_data(data, status_code=200):
    return jsonify({"data": data, "code": status_code}), status_code


def generate_random_str(length=30):
    return "".join([choice(ascii_letters) for _ in range(length)])
