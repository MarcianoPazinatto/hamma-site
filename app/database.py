from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import get_settings

settings = get_settings()

# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {},
    pool_pre_ping=True,  # Verify connections before using them
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

from .models import Base  # Import Base after engine creation

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables and run migrations if needed"""
    # Create all tables from models
    Base.metadata.create_all(bind=engine)
