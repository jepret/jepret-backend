from flask import request, g

from core.error import BaseError
from service.nlp import analyze_sentiment
from core.util import *
from model import Verification, QuestionAnswer, UMKM, UMKMStatistic


def create_verification():
    data = request.json
    verification = Verification.get_or_none(
        (Verification.umkm == data['umkm']) &
        (Verification.verifier == g.user['id'])
    )
    if verification:
        raise BaseError("You have already verified this place.", 400)

    umkm = UMKM.get_or_none(UMKM.id == data['umkm'])
    if not umkm:
        raise BaseError("UMKM not found", 404)

    verification_data = data.copy()
    verification_data['verifier'] = g.user['id']
    del verification_data['qas']

    verification = Verification(**verification_data)

    stat = UMKMStatistic.get_or_none(UMKMStatistic.umkm == umkm)
    if not stat:
        stat = UMKMStatistic(umkm=umkm)
        stat.save()

    result = analyze_sentiment(verification.review)
    if result == 0:
        stat.neutral_review_count += 1
        verification.sentiment = "neutral"
    elif result == 1:
        stat.positive_review_count += 1
        verification.sentiment = "positive"
    else:
        verification.sentiment = "negative"
        stat.negative_review_count += 1

    verification.save()
    stat.save()

    items = []
    for qa in data['qas']:
        qa['verification'] = verification.id
        item = QuestionAnswer(**qa)
        item.save()
        items.append(item.to_dict())

    result = verification.to_dict()
    result["qas"] = items

    return respond_data(result)


def get_verification_by_id(v_id):
    verification = Verification.get_or_none(Verification.id == v_id)
    if not verification:
        raise BaseError("Verification not found", 404)

    return respond_data(verification.to_dict())
