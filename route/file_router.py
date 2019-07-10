from core.router import Router

import handler.file as handler
from middleware.auth import AuthMiddleware


upload_file = AuthMiddleware()
upload_file = upload_file.add_next(handler.upload_file)


get_file = AuthMiddleware()
get_file = get_file.add_next(handler.get_file)

router = Router("/file")
router.route("/<unique_id>", get_file)
router.route("/", upload_file, methods=["POST"])
