from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

user_v1 = APIRouter()

# @user_v1.get("/users", response_model=list[User])
# def get_users_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), request: Request = None):
#     request.state.response_message = 'Testing response message'
#     return get_users_service(db=db, skip=skip, limit=limit)
#
#
# @user_v1.post("/users", response_model=User)
# def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
#     return create_user_service(db=db, user=user)
#

# @user_v1.post("/users")
# def create_user_route(user: UserCreate, db: Session = Depends(get_db)):
#     return create_user(db=db, user=user)
#

# @user_v1.get("/users/{user_id}")
# def get_user_route(user_id: int, db: Session = Depends(get_db)):
#     user = get_user_by_id(db=db, user_id=user_id)
#     if user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user
#
#
# @user_v1.put("/users/{user_id}")
# def update_user_route(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
#     updated_user = update_user(db=db, user_id=user_id, user_data=user)
#     if updated_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return updated_user
#
#
# @user_v1.delete("/users/{user_id}")
# def delete_user_route(user_id: int, db: Session = Depends(get_db)):
#     deleted_user = delete_user(db=db, user_id=user_id)
#     if deleted_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return {"message": "User deleted successfully"}
