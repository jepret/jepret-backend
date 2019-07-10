from datetime import datetime
from flask import request, g

from core.error import BaseError
from core.util import *
from model import UMKM


def create_UMKM():
    data = request.json
    data['founding_date'] = datetime.strptime(data['founding_date'], '%Y-%m-%d')
    data['owner'] = g.user["id"]

    umkm = UMKM(**data)
    umkm.save()

    return respond_data(umkm.to_dict(exclude_balance=False))


def delete_UMKM():
    data = request.json
    umkm = UMKM.get_or_none((UMKM.id == data['id']) & (UMKM.owner == g.user['id']))
    if not umkm:
        raise BaseError("UMKM not found", 404)

    umkm.delete_instance()
    return respond_data(umkm.to_dict(exclude_balance=False))


def get_UMKM(umkm_id):
    umkm = UMKM.get_or_none(UMKM.id == umkm_id)
    if not umkm:
        raise BaseError("UMKM not found", 404)

    return respond_data(umkm.to_dict(exclude_balance=umkm.owner.id != g.user['id']))


def nearby_UMKM():
    data = request.json
    lat = float(data['lat'])
    lng = float(data['lng'])
    umkms = UMKM.select()
    umkms = sorted(umkms, key=lambda x: (x.lat - lat) ** 2 + (x.lng - lng) ** 2)
    umkms = list(map(lambda x: x.to_dict(), umkms))

    return respond_data(umkms)
