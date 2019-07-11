from route.user import router as user_router
from route.UMKM import router as UMKM_router
from route.file import router as file_router
from route.verification import router as verification_router
from route.statistic import router as statistic_router
from route.transaction import router as transaction_router
from route.UMKM_detail import router as UMKM_detail_router

routers = [
    user_router,
    UMKM_router,
    file_router,
    verification_router,
    statistic_router,
    transaction_router,
    UMKM_detail_router
]
