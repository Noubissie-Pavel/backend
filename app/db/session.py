from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from app.core.config import DATABASE_URL  # ensure this has the async URL

# Create the async engine using the async URL
engine = create_async_engine(DATABASE_URL, echo=True)

# Create an async session maker
SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

# Dependency to provide an async session
async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        yield session

Base = declarative_base()
