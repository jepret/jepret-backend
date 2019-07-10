from flask import request, g

from core.error import BaseError
from redis_model import Session
from core.util import *
from model import User


def register():
    data = request.json
    user = User.get_or_none(
        (User.id_card == data["id_card"]) | (User.phone_number == data["phone_number"])
    )
    if user:
        raise BaseError("ID Card / Phone number already exists", 400)

    user = User(**data)
    user.save()

    token = generate_random_str(30)
    session = Session(token, user.to_dict())
    session.save()

    result = user.to_dict()
    result["auth_token"] = token

    return respond_data(result)


def login():
    data = request.json
    password = User.hash(data["password"])
    user = User.get_or_none(
        (User.id_card == data["id_card"]) & (User.password == password)
    )
    if not user:
        raise BaseError("Invalid ID Card / password", 404)

    token = generate_random_str(30)
    session = Session(token, user.to_dict())
    session.save()

    result = user.to_dict()
    result["auth_token"] = token

    return respond_data(result)


def profile():
    user = User.get_or_none(User.id == g.user['id'])
    return respond_data(user.to_dict())
