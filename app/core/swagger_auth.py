from fastapi import HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.core.config import SWAGGER_USERNAME, SWAGGER_PASSWORD
from app.core.exceptions import raise_invalid_credentials

security = HTTPBasic()


def swagger_authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != SWAGGER_USERNAME or credentials.password != SWAGGER_PASSWORD:
        raise_invalid_credentials()
    return credentials
