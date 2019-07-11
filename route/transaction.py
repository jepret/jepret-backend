from core.validator import BaseValidator
from core.router import Router

import handler.transaction as handler
from middleware.auth import AuthMiddleware


def check_amount(field, value, error):
    if value <= 0:
        error(field, "Must be positive")

create_transaction = AuthMiddleware()
create_transaction = create_transaction.add_next(
    BaseValidator({
        "amount": {
            "type": "integer",
            "required": True,
            "check_with": check_amount
        },
        "umkm_uid": {
            "type": "string",
            "required": True
        }
    })
)
create_transaction = create_transaction.add_next(handler.create_transaction)

router = Router("/transaction")
router.route("/", create_transaction, methods=["POST"])
