"""
Aplicación principal FastAPI
"""
from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.core.config import settings
from app.db.session import engine, Base, SessionLocal
from app.routers import users, items

# Configurar logging
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan para inicializar y probar la conexión a la base de datos.
    Se ejecuta al iniciar y cerrar la aplicación.
    """
    # Startup: Inicializar base de datos
    logger.info("Inicializando base de datos...")
    
    try:
        # Crear las tablas si no existen
        Base.metadata.create_all(bind=engine)
        logger.info("Tablas de base de datos creadas/verificadas")
        
        # Probar la conexión
        with SessionLocal() as db:
            result = db.execute(text("SELECT 1"))
            result.scalar()
            logger.info("Conexión a la base de datos verificada correctamente")
            
    except Exception as e:
        logger.error(f"Error al inicializar la base de datos: {e}")
        raise
    
    yield
    
    # Shutdown: Cerrar conexiones
    logger.info("Cerrando conexiones a la base de datos...")
    engine.dispose()
    logger.info("Conexiones cerradas")


# Crear la aplicación FastAPI con lifespan
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan,
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(users.router, prefix="/api/v1")
app.include_router(items.router, prefix="/api/v1")


@app.get("/")
def read_root():
    """Endpoint raíz"""
    return {
        "message": f"Bienvenido a {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    """Endpoint de verificación de salud"""
    return {"status": "healthy"}

