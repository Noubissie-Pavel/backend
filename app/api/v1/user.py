from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.user import User, UserCreate
from app.services.user import get_users_service, create_user_service, get_user_by_id_service, update_user_service, \
    delete_user_service
from app.utils.utils import PAGE_LIMIT

user_v1 = APIRouter()


@user_v1.get("/users", response_model=list[User])
async def get_users_endpoint(skip: int = 0, limit: int = PAGE_LIMIT, db: AsyncSession = Depends(get_db),
                             request: Request = None):
    try:
        request.state.response_message = f'All User data. {skip} - {limit}'
        return await get_users_service(db, skip, limit)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@user_v1.get("/users/{user_id}", response_model=User)
async def get_one_user_endpoint(user_id: int, db: AsyncSession = Depends(get_db), request: Request = None):
    try:
        response = await get_user_by_id_service(db, user_id)
        request.state.response_message = f'User with id {user_id} fetched successfully'
        if response is None:
            raise HTTPException(status_code=404, detail=f"User with id {user_id} not found.")
        return response
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@user_v1.post("/users", response_model=User)
async def create_user_endpoint(user: UserCreate, db: AsyncSession = Depends(get_db), request: Request = None):
    try:
        request.state.response_message = 'User created successfully'
        return await create_user_service(db, user)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@user_v1.put("/users/{user_id}", response_model=User)
async def update_user_endpoint(user_id: int, user: UserCreate, db: AsyncSession = Depends(get_db),
                               request: Request = None):
    try:
        response = await update_user_service(db, user_id, user)
        request.state.response_message = f'User with id {user_id} updated successfully'
        if response is None:
            raise HTTPException(status_code=404, detail=f"User with id {user_id} not found.")
        return response
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@user_v1.delete("/users/{user_id}", response_model=User)
async def delete_user_endpoint(user_id: int, db: AsyncSession = Depends(get_db), request: Request = None):
    try:
        response = await delete_user_service(db, user_id)
        request.state.response_message = f'User with id {user_id} deleted successfully'
        if response is None:
            raise HTTPException(status_code=404, detail=f"User with id {user_id} not found.")
        return response
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
