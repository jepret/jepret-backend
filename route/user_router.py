from core.router import Router
from core.validator import BaseValidator

import handler.user_handler as handler


register = BaseValidator(
    {
        "name": {"type": "string", "required": True, "empty": False},
        "id_card": {"type": "string", "required": True, "empty": False},
        "phone_number": {"type": "string", "required": True, "empty": False},
        "password": {"type": "string", "required": True, "empty": False},
    }
)
register = register.add_next(handler.register)

login = BaseValidator(
    {
        "id_card": {"type": "string", "required": True, "empty": False},
        "password": {"type": "string", "required": True, "empty": False},
    }
)
login = login.add_next(handler.login)

router = Router("/user")
router.route("/login", login, methods=["POST"])
router.route("/register", register, methods=["POST"])
