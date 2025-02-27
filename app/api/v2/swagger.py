import uvicorn
from fastapi import APIRouter
from fastapi import FastAPI, Depends
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

from app.core.swagger_auth import swagger_authenticate_user

swagger_v2 = APIRouter()


@swagger_v2.get("/docs", dependencies=[Depends(swagger_authenticate_user)])
async def get_swagger():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="Swagger UI")


@swagger_v2.get("/openapi.json", dependencies=[Depends(swagger_authenticate_user)])
async def get_open_api_endpoint():
    return get_openapi(title=swagger_v2.title, version=swagger_v2.version, description=swagger_v2.description, routes=swagger_v2.routes)
