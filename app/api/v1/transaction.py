from app.schemas.transaction import TransactionSchema, TransactionCreateSchema
from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.transaction import get_transactions_service, create_transaction_service, get_transaction_by_id_service

transaction_v1 = APIRouter()


@transaction_v1.post("/transaction", response_model=TransactionSchema)
async def create_transaction_endpoint(transaction_data: TransactionCreateSchema, db: AsyncSession = Depends(get_db),
                                      request: Request = None):
    try:
        new_operator = await create_transaction_service(db, transaction_data=transaction_data)
        request.state.response_message = "Transaction created successfully"
        return new_operator
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@transaction_v1.get("/transaction", response_model=list[TransactionSchema])
async def get_transactions_endpoint(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db),
                                    request: Request = None):
    try:
        request.state.response_message = 'Transaction response message'
        return await get_transactions_service(db=db, skip=skip, limit=limit)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@transaction_v1.get("/transaction/{transaction_id}")
async def get_transaction_route(transaction_id: int, db: AsyncSession = Depends(get_db)):
    transaction = await get_transaction_by_id_service(db=db, transaction_id=transaction_id)
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction data not found")
    return ["ok"]
