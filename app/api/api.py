from fastapi import APIRouter
from .endpoints import users,payment,costs,validate, videos

api_router = APIRouter()

api_router.include_router(users.router)
api_router.include_router(videos.router)
api_router.include_router(costs.router)
api_router.include_router(payment.router)
api_router.include_router(validate.router)

