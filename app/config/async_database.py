from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.config.settings import settings
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession



SQLALCHEMY_DATABASE_URL = f'postgresql+asyncpg://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}'

# Create async engine
async_engine = create_async_engine(
    url=SQLALCHEMY_DATABASE_URL,
    # echo=True,  # Set to True to enable SQL logging for debugging
    pool_pre_ping=True,
    pool_recycle=3600,
    pool_size=20,
    max_overflow=0
)

# Async session factory
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False
)

Base = declarative_base()


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session