from core.router import Router
from core.validator import BaseValidator

import handler.verification as handler
from middleware.auth import AuthMiddleware


create_verification = AuthMiddleware()
create_verification = create_verification.add_next(
    BaseValidator({
        "umkm": {
            "type": "integer",
            "required": True
        },
        "photo": {
            "type": "string",
            "required": True,
            "empty": False
        },
        "star": {
            "type": "integer",
            "required": False
        },
        "review": {
            "type": "string",
            "required": False,
            "empty": False
        },
        "qas": {
            "type": "list",
            "required": True,
            "empty": False
        }
    })
)
create_verification = create_verification.add_next(handler.create_verification)

get_verification_by_id = AuthMiddleware().add_next(handler.get_verification_by_id)

router = Router("/verification")
router.route("/", create_verification, methods=["POST"])
router.route("/<v_id>", get_verification_by_id)
