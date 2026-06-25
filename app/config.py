from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Configurações da aplicação"""
    
    # Informações da aplicação
    APP_NAME: str = "Hama Sharing App App"
    APP_VERSION: str = "1.0.0"
    
    # Banco de dados
    DATABASE_URL: str = "sqlite:///./app.db"
    
    # Autenticação
    SECRET_KEY: str = "sua-chave-secreta-super-segura-mude-isto-em-producao"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Upload de arquivos
    UPLOAD_DIRECTORY: str = "app/static/uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB em bytes
    ALLOWED_EXTENSIONS: list = ["jpeg", "png", "gif", "webp"]
    
    # CORS
    CORS_ORIGINS: list = ["*"]
    
    # Ambiente
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache()
def get_settings():
    """Retorna a instância de configurações (com cache)"""
    return Settings()
