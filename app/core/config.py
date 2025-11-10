"""
Configuración de la aplicación usando variables de entorno
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Configuración de la aplicación"""
    
    # Configuración de la aplicación
    APP_NAME: str = "FastAPI Template"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False
    
    # Configuración de la base de datos
    DATABASE_URL: str = "sqlite:///./app.db"
    
    # Configuración de seguridad
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Configuración de CORS
    CORS_ORIGINS: list[str] = ["*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Instancia global de configuración
settings = Settings()

