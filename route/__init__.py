from route.user import router as user_router
from route.UMKM import router as UMKM_router
from route.file import router as file_router
from route.verification import router as verification_router

routers = [user_router, UMKM_router, file_router, verification_router]
