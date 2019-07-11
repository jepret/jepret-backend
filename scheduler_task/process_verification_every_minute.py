import dotenv
dotenv.load_dotenv()

from time import sleep
import schedule
import requests
import json

from service.image_recognition import check_image_similarity
from model import UMKM, UMKMValidator, Verification


def get_base_images(umkm):
    validator = UMKMValidator.get_or_none(UMKMValidator.umkm == umkm)
    if not validator:
        return []

    return json.loads(validator.seed_images)


def get_verifications(umkm):
    verifications = Verification.select().where((Verification.umkm == umkm) & (Verification.pending == True))
    return verifications


def is_verification_valid(verification, seed_images):
    r = requests.get(verification.photo)
    photo = r.content
    count = 0
    for s in seed_images:
        with open(s, 'rb') as f:
            distance = check_image_similarity(f, photo)
            if distance < 30:
                count += 1
            if count == 3:
                return True

    return False


def process_verifications():
    umkms = UMKM.select()
    for u in umkms:
        verifications = get_verifications(u)
        seed_images = get_base_images(u)
        if not seed_images:
            continue
        for v in verifications:
            v.success = is_verification_valid(v, seed_images)
            v.pending = False
            v.save()


schedule.every().minute.do(process_verifications)


while True:
    try:
        schedule.run_pending()
    except:
        pass
    finally:
        sleep(1)
