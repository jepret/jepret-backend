from core.router import Router

import handler.statistic as handler
from middleware.auth import AuthMiddleware


get_umkm_statistic = AuthMiddleware().add_next(handler.get_umkm_statistic)

router = Router("/stat")
router.route("/umkm/<umkm_id>", get_umkm_statistic)
