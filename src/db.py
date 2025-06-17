from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models import Base
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./db.sqlite3")


engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

Base.metadata.create_all(bind=engine)
