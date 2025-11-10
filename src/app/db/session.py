"""
Configuración de la sesión de base de datos
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# Crear el motor de la base de datos
# Si DATABASE_URL no especifica el driver, usar psycopg (versión 3)
database_url = settings.DATABASE_URL
if database_url.startswith("postgresql://") and "+" not in database_url:
    # Reemplazar postgresql:// por postgresql+psycopg:// para usar psycopg v3
    database_url = database_url.replace("postgresql://", "postgresql+psycopg://", 1)

engine = create_engine(
    database_url,
    pool_pre_ping=True,  # Verifica conexiones antes de usarlas
    echo=settings.DEBUG,  # Muestra queries SQL en modo debug
)

# Crear la clase base para los modelos
Base = declarative_base()

# Crear la fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    Dependencia para obtener la sesión de base de datos.
    Uso en routers:
        @app.get("/items")
        def read_items(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

