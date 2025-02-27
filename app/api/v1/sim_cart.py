from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.sim_cart import SimCart
from app.schemas.sim_cart import SimCartCreate, SimCartUpdate
from app.services.sim_cart import create_sim_cart_service, get_sim_carts_service, get_sim_cart_by_id_service, \
    update_sim_cart_service, delete_sim_cart_service

sim_cart_v1 = APIRouter()


@sim_cart_v1.get("/sim_cart", response_model=list[SimCart])
def get_sim_carts_endpoint(db: Session = Depends(get_db), skip: int = 0, limit: int = 100, request: Request = None):
    request.state.response_message = 'Sim cart response message'
    return get_sim_carts_service(db=db, skip=skip, limit=limit)


@sim_cart_v1.post("/sim_cart", response_model=SimCart)
def create_sim_cart_endpoint(sim_cart: SimCartCreate, request: Request = None, db: Session = Depends(get_db)):
    try:
        new_operator = create_sim_cart_service(db=db, sim_cart=sim_cart)
        request.state.response_message = "Sim cart created successfully"
        return new_operator
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@sim_cart_v1.get("/sim_cart/{sim_cart_id}")
def get_sim_cart_route(sim_cart_id: int, db: Session = Depends(get_db)):
    sim_cart = get_sim_cart_by_id_service(db=db, sim_cart_id=sim_cart_id)
    if sim_cart is None:
        raise HTTPException(status_code=404, detail="Sim cart not found")
    return sim_cart


@sim_cart_v1.put("/sim_cart/{sim_cart_id}")
def update_sim_cart_route(sim_cart_id: int, sim_cart: SimCartUpdate, db: Session = Depends(get_db),
                          request: Request = None):
    request.state.response_message = 'Update sim cart successfully'
    telecom_operator = update_sim_cart_service(db=db, sim_cart_id=sim_cart_id, sim_cart=sim_cart)
    if telecom_operator is None:
        raise HTTPException(status_code=404, detail="Sim cart not found")
    return telecom_operator


@sim_cart_v1.delete("/sim_cart/{sim_cart_id}")
def delete_sim_cart_route(sim_cart_id: int, db: Session = Depends(get_db)):
    telecom_operator = delete_sim_cart_service(db=db, sim_cart_id=sim_cart_id)
    if telecom_operator is None:
        raise HTTPException(status_code=404, detail="Sim cart not found")
    return telecom_operator
