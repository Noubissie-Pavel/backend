import uvicorn
from fastapi import FastAPI, Depends
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

from app.api.base import router
from app.core.config import PORT
from app.db.session import SessionLocal
from app.middleware.pagination import ResponseFormattingMiddleware
from app.services.user import create_default_admin

app = FastAPI(
    title="EU Backup",
    description="Some description about this project",
    version="1.0.0",
    docs_url=None,
    redoc_url=None,
    openapi_url="/openapi.json"
)

app.add_middleware(ResponseFormattingMiddleware)

app.include_router(router)


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()


@app.on_event("startup")
async def startup_event():
    async for db in get_db():
        await create_default_admin(db)


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", reload=True, port=PORT)
