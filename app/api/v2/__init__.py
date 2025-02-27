from fastapi import APIRouter

from app.api.v2.swagger import swagger_v2
from app.api.v2.user import users_v2

router = APIRouter(prefix="/v2")

router.include_router(swagger_v2)
router.include_router(users_v2)
