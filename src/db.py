from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from src.models import Base
from src.config import settings

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

engine = create_engine(
    str(settings.database_url), 
    connect_args={"check_same_thread": False},
    echo=settings.debug
)

SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

Base.metadata.create_all(bind=engine)
