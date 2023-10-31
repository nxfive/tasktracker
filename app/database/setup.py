from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from typing import Generator, Any
from app.core.config import get_settings


Base = declarative_base()


def get_engine() -> Engine:
    settings = get_settings()
    return create_engine(str(settings.database_url), future=True)


def get_session() -> Session:
    return sessionmaker(autocommit=False, autoflush=False, bind=get_engine())()


def get_db() -> Generator[Session, Any, None]:
    db = get_session()
    try:
        yield db
    finally:
        db.close()
