from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.ussd import Ussd, UssdCreate, UssdUpdate
from app.services.ussd import get_ussd_service, create_ussd_service, get_ussd_by_id_service, update_ussd_service, \
    delete_ussd_service

ussd_v1 = APIRouter()


@ussd_v1.get("/ussd", response_model=list[Ussd])
async def get_ussd_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                            request: Request = None):
    try:
        request.state.response_message = 'Ussd response message'
        return await get_ussd_service(db=db, skip=skip, limit=limit)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@ussd_v1.post("/ussd", response_model=Ussd)
def create_ussd_endpoint(ussd_data: UssdCreate, db: Session = Depends(get_db),
                         request: Request = None):
    try:
        new_operator = create_ussd_service(db=db, ussd_data=ussd_data)
        request.state.response_message = "Ussd created successfully"
        return new_operator
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@ussd_v1.get("/ussd/{ussd_id}")
def get_ussd_route(ussd_id: int, db: Session = Depends(get_db)):
    ussd = get_ussd_by_id_service(db=db, ussd_id=ussd_id)
    if ussd is None:
        raise HTTPException(status_code=404, detail="Ussd data not found")
    return ussd


@ussd_v1.put("/ussd/{ussd_id}")
def update_ussd_route(ussd_id: int, ussd: UssdUpdate,
                      db: Session = Depends(get_db)):
    ussd = update_ussd_service(db=db, ussd_id=ussd_id, ussd_data=ussd)
    if ussd is None:
        raise HTTPException(status_code=404, detail="Ussd not found")
    return ussd


@ussd_v1.delete("/ussd/{ussd_id}")
def delete_ussd_route(ussd_id: int, db: Session = Depends(get_db)):
    ussd = delete_ussd_service(db=db, ussd_id=ussd_id)
    if ussd is None:
        raise HTTPException(status_code=404, detail="Ussd not found")
    return ussd
