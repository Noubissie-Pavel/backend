from datetime import datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.sim_cart import SimCart
from app.schemas.sim_cart import SimCartCreate, SimCartUpdate


def create_sim_cart(sim_cart: SimCartCreate, db: Session, ):
    db_sim_cart = SimCart(
        phone_number=sim_cart.phone_number,
        description=sim_cart.description,
        is_active=sim_cart.is_active,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    try:
        db.add(db_sim_cart)
        db.commit()
        db.refresh(db_sim_cart)
        return db_sim_cart
    except IntegrityError:
        db.rollback()
        raise ValueError(f"Sim Cart with phone number {sim_cart.operator_name} already exists.")


def get_sim_carts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(SimCart).offset(skip).limit(limit).all()


def get_sim_cart_by_id(sim_cart_id: int, db: Session, ):
    return db.query(SimCart).filter(SimCart.id == sim_cart_id).first()


def update_sim_cart(sim_cart_id: int, sim_cart_data: SimCartUpdate, db: Session):
    db_sim_cart = db.query(SimCart).filter(SimCart.id == sim_cart_id).first()
    if db_sim_cart:
        db_sim_cart.phone_number = sim_cart_data.phone_number or db_sim_cart.phone_number
        db_sim_cart.description = sim_cart_data.description or db_sim_cart.description
        db_sim_cart.is_active = sim_cart_data.is_active or db_sim_cart.is_active
        db_sim_cart.updated_at = datetime.now()
        try:
            db.commit()
            db.refresh(db_sim_cart)
            return db_sim_cart
        except IntegrityError:
            db.rollback()
            raise ValueError(f"Sim Cart with phone number  {sim_cart_data.operator_name} already exists.")
    return None


def delete_sim_cart(sim_cart_id: int, db: Session):
    db_sim_cart = db.query(SimCart).filter(
        SimCart.id == sim_cart_id).first()
    if db_sim_cart:
        db.delete(db_sim_cart)
        db.commit()
        return db_sim_cart
    return None
