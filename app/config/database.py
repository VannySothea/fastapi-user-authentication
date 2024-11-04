from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.config.settings import settings
from typing import Generator


SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}'

engine = create_engine(url=SQLALCHEMY_DATABASE_URL,
                       pool_pre_ping=True,
                       pool_recycle=3600,
                       pool_size=20,
                       max_overflow=0)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_session() -> Generator:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()