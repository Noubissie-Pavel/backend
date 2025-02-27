from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session

from app.controller.telecom_operator import get_telecom_operator_by_id, update_telecom_operator, \
    get_telecom_operators, delete_telecom_operator
from app.db.session import get_db
from app.schemas.telecom_operator import TelecomOperator
from app.schemas.telecom_operator import TelecomOperatorCreate, TelecomOperatorUpdate
from app.services.telocom_operator import create_telecom_operator_service, get_telecom_operators_service, \
    get_telecom_operator_by_id_service

telecom_operator_v1 = APIRouter()


@telecom_operator_v1.get("/telecom_operator", response_model=list[TelecomOperator])
def get_telecom_operators_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                                   request: Request = None):
    try:
        request.state.response_message = 'Telecom Operator response message'
        return get_telecom_operators_service(db=db, skip=skip, limit=limit)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, message=str(e))


@telecom_operator_v1.post("/telecom_operator", response_model=TelecomOperator)
def create_telecom_operator_endpoint(telecom_operator: TelecomOperatorCreate, db: Session = Depends(get_db),
                                     request: Request = None):
    try:
        new_operator = create_telecom_operator_service(db=db, telecom_operator=telecom_operator)
        request.state.response_message = "Telecom Operator created successfully"
        return new_operator
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@telecom_operator_v1.get("/telecom_operator/{telecom_operator_id}")
def get_telecom_operator_route(telecom_operator_id: int, db: Session = Depends(get_db)):
    telecom_operator = get_telecom_operator_by_id_service(db=db, telecom_operator_id=telecom_operator_id)
    if telecom_operator is None:
        raise HTTPException(status_code=404, detail="Telecom operator not found")
    return telecom_operator


@telecom_operator_v1.put("/telecom_operator/{telecom_operator_id}")
def update_telecom_operator_route(telecom_operator_id: int, telecom_operator: TelecomOperatorUpdate,
                                  db: Session = Depends(get_db)):
    telecom_operator = update_telecom_operator(db=db, telecom_operator_id=telecom_operator_id,
                                               telecom_operator_data=telecom_operator)
    if telecom_operator is None:
        raise HTTPException(status_code=404, detail="Telecom Operator not found")
    return telecom_operator


@telecom_operator_v1.delete("/telecom_operator/{telecom_operator_id}")
def delete_telecom_operator_route(telecom_operator_id: int, db: Session = Depends(get_db)):
    telecom_operator = delete_telecom_operator(db=db, telecom_operator_id=telecom_operator_id)
    if telecom_operator is None:
        raise HTTPException(status_code=404, detail="Telecom Operator not found")
    return telecom_operator
