from core.router import Router
from core.validator import BaseValidator

import handler.UMKM as handler
from middleware.auth import AuthMiddleware

create_UMKM = AuthMiddleware()
create_UMKM = create_UMKM.add_next(
    BaseValidator({
        "name": {
            "type": "string",
            "required": True,
            "empty": False
        },
        "photo": {
            "type": "string",
            "required": True,
            "empty": False
        },
        "lat": {
            "type": "float",
            "required": True
        },
        "lng": {
            "type": "float",
            "required": True
        },
        "sector": {
            "type": "string",
            "required": True,
            "empty": False
        },
        "address": {
            "type": "string",
            "required": True,
            "empty": False
        },
        "city": {
            "type": "string",
            "required": True,
            "empty": False
        },
        "province": {
            "type": "string",
            "required": True,
            "empty": False
        },
        "founding_date": {
            "type": "string",
            "required": True,
            "empty": False
        }
    })
)
create_UMKM = create_UMKM.add_next(handler.create_UMKM)

delete_UMKM = AuthMiddleware()
delete_UMKM = delete_UMKM.add_next(
    BaseValidator({
        "id": {
            "type": "integer",
            "required": True,
        }
    })
)
delete_UMKM = delete_UMKM.add_next(handler.delete_UMKM)

get_UMKM = AuthMiddleware()
get_UMKM = get_UMKM.add_next(handler.get_UMKM)

nearby_UMKM = AuthMiddleware()
nearby_UMKM = nearby_UMKM.add_next(
    BaseValidator({
        "lat": {
            "type": "float",
            "required": True
        },
        "lng": {
            "type": "float",
            "required": True
        }
    })
)
nearby_UMKM = nearby_UMKM.add_next(handler.nearby_UMKM)
get_qr = AuthMiddleware().add_next(handler.get_qr)
get_verifications = AuthMiddleware().add_next(handler.get_verifications)

router = Router("/umkm")
router.route("/<umkm_id>", get_UMKM)
router.route("/", create_UMKM, methods=["POST"])
router.route("/nearby", nearby_UMKM, methods=["POST"])
router.route("/<umkm_id>/qr", get_qr)
router.route("/delete", delete_UMKM, methods=["POST"])
router.route("/verification", get_verifications)
