from core.router import Router
from core.validator import BaseValidator

from handler.test_handler import *

post_endpoint = BaseValidator(
    {"name": {"type": "string", "required": True, "empty": False}}
)
post_endpoint = post_endpoint.add_next(test_post)

router = Router("")
router.route("/<name>", test_get)
router.route("/", post_endpoint, methods=["POST"])
