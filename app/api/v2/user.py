from fastapi import APIRouter

users_v2 = APIRouter()


@users_v2.get("/users/me")
async def read_users_me():
    return {"user_id": "the current user from version 2"}
