from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from .config import get_settings
import os

# Obter configurações
settings = get_settings()

# Usar DATABASE_URL do ambiente (PostgreSQL em produção) ou SQLite em desenvolvimento
DATABASE_URL = os.getenv("DATABASE_URL", settings.DATABASE_URL)

# Converter postgres:// para postgresql:// se necessário (Render usa postgres://)
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Configurar argumentos de conexão baseado no tipo de banco
if DATABASE_URL.startswith("postgresql"):
    # PostgreSQL
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,  # Verifica conexões antes de usar
        pool_size=10,
        max_overflow=20,
    )
else:
    # SQLite (desenvolvimento)
    engine = create_engine(
        DATABASE_URL, 
        connect_args={"check_same_thread": False}
    )

SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
