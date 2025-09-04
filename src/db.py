from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from src.models import Base
from src.config import settings

# Create the SQLAlchemy engine using the database URL from settings
engine = create_engine(
    str(settings.database_url),
    echo=settings.debug  # Enable SQL query logging if debug is True
)

# Create a configured "Session" class
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Create all tables in the database
Base.metadata.create_all(bind=engine)

def get_db() -> Generator[Session, None, None]:
    """
    Dependency that provides a database session.
    Yields a SQLAlchemy Session and ensures it is closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
