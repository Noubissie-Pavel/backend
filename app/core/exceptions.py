from fastapi import HTTPException

from app.core.status_codes import HTTP_401_UNAUTHORIZED


def raise_invalid_credentials():
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
