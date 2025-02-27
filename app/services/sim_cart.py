from sqlalchemy.orm import Session

from app.crud.sim_cart import create_sim_cart, get_sim_carts, get_sim_cart_by_id, update_sim_cart, delete_sim_cart
from app.schemas.sim_cart import SimCartCreate, SimCartUpdate


def create_sim_cart_service(sim_cart: SimCartCreate, db: Session, ):
    return create_sim_cart(sim_cart=sim_cart, db=db)


def get_sim_carts_service(db: Session, skip: int = 0, limit: int = 100):
    return get_sim_carts(skip=skip, limit=limit, db=db)


def get_sim_cart_by_id_service(sim_cart_id: int, db: Session, ):
    return get_sim_cart_by_id(sim_cart_id=sim_cart_id, db=db)


def update_sim_cart_service(sim_cart_id: int, sim_cart: SimCartUpdate, db: Session, ):
    return update_sim_cart(sim_cart_id=sim_cart_id, sim_cart_data=sim_cart, db=db)


def delete_sim_cart_service(sim_cart_id: int, db: Session, ):
    return delete_sim_cart(sim_cart_id=sim_cart_id, db=db)
