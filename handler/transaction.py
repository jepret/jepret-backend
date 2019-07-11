from flask import request, g

from core.error import BaseError
from core.util import *
from model import Transaction, UMKM, User


def create_transaction():
    data = request.json
    umkm = UMKM.get_or_none(UMKM.unique_id == data['umkm_uid'])
    if not umkm:
        raise BaseError("UMKM not found", 404)

    user = User.get_or_none(User.id == g.user['id'])
    if not user:
        raise BaseError("Unauthorized", 401)

    if data['amount'] > user.balance:
        raise BaseError("Not enough balance", 400)

    user.balance -= data['amount']
    user.save()

    umkm.balance += data['amount']
    umkm.save()

    transaction = Transaction(
        sender=user,
        receiver=umkm,
        amount=data['amount']
    )
    transaction.save()

    return respond_data(transaction.to_dict())
