"""
Script to initialize the database tables on Supabase.
Run this once after setting up Supabase database.
"""

from src.models import Base
from src.db import engine
from src.config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_database():
    """Create all tables in the database"""
    try:
        logger.info(f"Connecting to database...")
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database tables created successfully!")
    except Exception as e:
        logger.error(f"❌ Error creating database tables: {e}")
        raise

if __name__ == "__main__":
    init_database()
