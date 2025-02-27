from fastapi import APIRouter

from app.api.v1.company import company_v1
from app.api.v1.sim_cart import sim_cart_v1
from app.api.v1.swagger import swagger_v1
from app.api.v1.telecom_operator import telecom_operator_v1
from app.api.v1.transaction import transaction_v1
from app.api.v1.user import user_v1
from app.api.v1.ussd import ussd_v1
from app.api.v2.swagger import swagger_v2
from app.api.v2.user import users_v2

router = APIRouter()

router.include_router(users_v2, prefix="/v2.0.0")

router.include_router(swagger_v2, prefix="/v2.0.0")

router.include_router(swagger_v1, prefix="/v1.0.0")

router.include_router(user_v1, prefix="/v1.0.0")

router.include_router(company_v1, prefix="/v1.0.0", tags=["company"])

router.include_router(telecom_operator_v1, prefix="/v1.0.0", tags=["telecom_operator"])

router.include_router(sim_cart_v1, prefix="/v1.0.0", tags=["sim_cart"])

router.include_router(ussd_v1, prefix="/v1.0.0", tags=["ussd"])

router.include_router(transaction_v1, prefix="/v1.0.0", tags=["transaction"])
