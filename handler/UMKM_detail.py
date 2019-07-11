from flask import request, g, Response

from core.error import BaseError
from core.util import *
from model import UMKMDetail, User


def create_umkm_detail():
    data = request.json
    user = User.get_or_none(User.id == g.user['id'])
    umkm = list(user.umkms)[0]
    if not umkm:
        raise BaseError("UMKM not found", 404)

    data['umkm_id'] = umkm.id
    umkm_detail = UMKMDetail(**data)
    umkm_detail.save()

    return respond_data(umkm_detail.to_dict())
