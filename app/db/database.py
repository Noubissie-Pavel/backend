from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.core.config import DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=True)

SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_db():
    async with SessionLocal() as session:
        yield session


Base = declarative_base()
