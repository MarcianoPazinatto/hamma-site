from sqlalchemy.orm import declarative_base

# Base class for all models - imported by both database.py and models.py
# This avoids circular imports
Base = declarative_base()
