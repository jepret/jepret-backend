import io
import qrcode
from datetime import datetime
from flask import request, g, Response

from core.error import BaseError
from core.util import *
from model import UMKM, Campaign


def create_UMKM():
    data = request.json
    data['founding_date'] = datetime.strptime(data['founding_date'], '%Y-%m-%d')
    data['owner'] = g.user["id"]

    umkm = UMKM(**data)
    umkm.save()

    campaign = Campaign(umkm=umkm)
    campaign.save()

    return respond_data(umkm.to_dict(exclude_balance=False))


def delete_UMKM():
    data = request.json
    umkm = UMKM.get_or_none((UMKM.id == data['id']) & (UMKM.owner == g.user['id']))
    if not umkm:
        raise BaseError("UMKM not found", 404)

    campaign = Campaign.get_or_none(Campaign.umkm == umkm)
    if campaign:
        campaign.delete_instance()

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
    umkms = [u for u in umkms if u.campaign[0].active]
    umkms = sorted(umkms, key=lambda x: (x.lat - lat) ** 2 + (x.lng - lng) ** 2)
    umkm_dicts = list(map(lambda x: x.to_dict(), umkms))
    for i, u in enumerate(umkm_dicts):
        budget = umkms[i].campaign[0].budget
        if budget > 300000:
            u['reward_level'] = 3
        elif budget > 200000:
            u['reward_level'] = 2
        elif budget > 100000:
            u['reward_level'] = 1
        else:
            u['reward_level'] = 0

    return respond_data(umkm_dicts)


def get_qr(umkm_id):
    umkm = UMKM.get_or_none(UMKM.id == umkm_id)
    if not umkm:
        raise BaseError("UMKM not found", 404)

    img = qrcode.make(umkm.unique_id)

    img_data = io.BytesIO()
    img.save(img_data, format='PNG')
    img_data = img_data.getvalue()

    return Response(img_data, mimetype="image/png")
