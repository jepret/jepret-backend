from core.router import Router
from core.validator import BaseValidator

import handler.user as handler
from middleware.auth import AuthMiddleware


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

'''
name = pw.CharField()
email = pw.CharField(default="")
id_card = pw.CharField(unique=True)
phone_number = pw.CharField(unique=True)
password = pw.CharField()
balance = pw.IntegerField(default=0)
'''
edit_profile = AuthMiddleware()
edit_profile = edit_profile.add_next(
    BaseValidator(
    {
        "name": {"type": "string", "required": True, "empty": False},
        "id_card": {"type": "string", "required": True, "empty": False},
        "phone_number": {"type": "string", "required": True, "empty": False},
        "password": {"type": "string", "required": True, "empty": False},
        "email": {"type": "string", "required": False, "empty": False},
    })
)
edit_profile = edit_profile.add_next(handler.edit_profile)


profile = AuthMiddleware().add_next(handler.profile)
verifications = AuthMiddleware().add_next(handler.verifications)
transactions = AuthMiddleware().add_next(handler.transactions)


router = Router("/user")
router.route("/login", login, methods=["POST"])
router.route("/register", register, methods=["POST"])
router.route("/profile", profile)
router.route("/profile/edit", edit_profile, methods=["POST"])
router.route("/verification", verifications)
router.route("/transaction", transactions)
