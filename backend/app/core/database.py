from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings
from app.core.logger import logger

# Database URL
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Database engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Models
Base = declarative_base()

# Dependency to get DB session
def get_db():
    # Create a new database session for each request
    db = SessionLocal()

    logger.info("Database session opened")

    try:
        yield db

    finally:
        db.close()
        logger.info("Database session closed")