from core.router import Router
from core.validator import BaseValidator

import handler.UMKM_detail as handler
from middleware.auth import AuthMiddleware


def validate_gender(field, value, error):
    if value != "m" and value != "f":
        error(field, "Gender only m/f")


def validate_rate(field, value, error):
    if value <= 0 or value > 5:
        error(field, "Rate 1- 5")


create_umkm_detail = AuthMiddleware()
create_umkm_detail = create_umkm_detail.add_next(
    BaseValidator({
        "owner_name": {
            "type": "string",
            "required": True,
            "empty": False
        },
        "position": {
            "type": "string",
            "required": True,
            "empty": False
        },
        "gender": {
            "type": "string",
            "required": True,
            "empty": False,
            "check_with": validate_gender
        },
        "birth_date": {
            "type": "string",
            "required": True,
            "empty": False
        },
        "expert_count": {
            "type": "integer",
            "required": True,
        },
        "worker_count": {
            "type": "integer",
            "required": True,
        },
        "gross_revenue": {
            "type": "integer",
            "required": True
        },
        "average_price": {
            "type": "integer",
            "required": True
        },
        "operational_cost": {
            "type": "integer",
            "required": True
        },
        "need_funding": {
            "type": "boolean",
            "required": True
        },
        "funding_amount": {
            "type": "integer",
            "required": True
        },
        "funding_month_count": {
            "type": "integer",
            "required": True
        },
        "money_eq_success": {
            "type": "integer",
            "required": True,
            "check_with": validate_rate
        },
        "money_eq_competence": {
            "type": "integer",
            "required": True,
            "check_with": validate_rate
        },
        "do_care_money": {
            "type": "integer",
            "required": True,
            "check_with": validate_rate
        },
    })
)

create_umkm_detail = create_umkm_detail.add_next(handler.create_umkm_detail)

router = Router("/umkm-detail")
router.route("/", create_umkm_detail, methods=["POST"])
