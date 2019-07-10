from flask import request, g

from core.error import BaseError
from core.util import *
from model import UMKMStatistic, UMKM


def get_umkm_statistic(umkm_id):
    umkm = UMKM.get_or_none((UMKM.id == umkm_id) & (UMKM.owner == g.user['id']))
    if not umkm:
        raise BaseError("UMKM not found", 404)

    stat = UMKMStatistic.get_or_none(UMKMStatistic.umkm == umkm)
    if not stat:
        stat = UMKMStatistic(umkm=umkm)
        stat.save()

    return respond_data(stat.to_dict())
