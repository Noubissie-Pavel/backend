from fastapi import APIRouter

from app.api.v1.swagger import swagger_v1
from app.api.v1.user import user_v1

router = APIRouter(prefix="/v1")

router.include_router(user_v1)
router.include_router(swagger_v1)
