# FastAPI Template

Plantilla base para proyectos FastAPI con estructura organizada y ejemplos mínimos funcionales.

## Estructura del Proyecto

```
fastapi-template/
├── src/
│   └── app/
│       ├── core/           # Configuración y seguridad
│       ├── db/
│       │   ├── models/     # Modelos SQLAlchemy (un archivo por modelo)
│       │   └── session.py  # Sesión y Base
│       ├── repositories/   # Acceso a datos
│       ├── routers/        # Endpoints de la API
│       ├── schemas/        # Schemas Pydantic
│       ├── services/       # Lógica de negocio
│       ├── utils/          # Utilidades
│       └── main.py         # Aplicación principal
├── tests/                  # Tests
├── .env                    # Variables de entorno
├── requirements.txt        # Dependencias
├── Dockerfile              # Configuración Docker
└── docker-compose.yml      # Docker Compose
```

## Características

- ✅ Estructura organizada y escalable
- ✅ Autenticación JWT
- ✅ Base de datos PostgreSQL con SQLAlchemy
- ✅ Lifespan para inicialización y verificación de BD
- ✅ Schemas Pydantic para validación
- ✅ Separación de responsabilidades (routers, services, repositories, schemas)
- ✅ Repositorios dedicados para acceso a datos
- ✅ Configuración mediante variables de entorno
- ✅ Docker y Docker Compose con PostgreSQL
- ✅ Tests de ejemplo

## Instalación

### Opción 1: Instalación Local

1. Crear un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Configurar variables de entorno:
```bash
# Crear archivo .env con la configuración de PostgreSQL
# DATABASE_URL=postgresql://user:password@localhost:5432/dbname
```

4. Asegúrate de tener PostgreSQL corriendo localmente o usa Docker Compose

5. Ejecutar la aplicación:
```bash
uvicorn src.app.main:app --reload
```

**Nota**: El lifespan de la aplicación verificará automáticamente la conexión a la base de datos al iniciar.

### Opción 2: Docker

1. Construir y ejecutar con Docker Compose:
```bash
docker-compose up --build
```

2. La aplicación estará disponible en: http://localhost:8000

## Uso

### Endpoints Disponibles

- `GET /` - Endpoint raíz
- `GET /health` - Verificación de salud
- `GET /docs` - Documentación interactiva (Swagger)
- `GET /redoc` - Documentación alternativa (ReDoc)

### API de Usuarios (`/api/v1/users`)

- `POST /api/v1/users/` - Crear usuario
- `GET /api/v1/users/` - Listar usuarios
- `GET /api/v1/users/{user_id}` - Obtener usuario
- `PUT /api/v1/users/{user_id}` - Actualizar usuario
- `DELETE /api/v1/users/{user_id}` - Eliminar usuario
- `POST /api/v1/users/login` - Autenticación (obtener token)

### API de Items (`/api/v1/items`)

- `POST /api/v1/items/` - Crear item
- `GET /api/v1/items/` - Listar items
- `GET /api/v1/items/{item_id}` - Obtener item
- `PUT /api/v1/items/{item_id}` - Actualizar item
- `DELETE /api/v1/items/{item_id}` - Eliminar item

## Ejemplos de Uso

### Crear un usuario

```bash
curl -X POST "http://localhost:8000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "usuario@example.com",
    "username": "usuario",
    "password": "contraseña123"
  }'
```

### Login

```bash
curl -X POST "http://localhost:8000/api/v1/users/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "usuario",
    "password": "contraseña123"
  }'
```

### Crear un item

```bash
curl -X POST "http://localhost:8000/api/v1/items/?owner_id=1" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Mi primer item",
    "description": "Descripción del item"
  }'
```

## Testing

Ejecutar tests:

```bash
pytest tests/
```

## Configuración

Las configuraciones se manejan mediante variables de entorno en el archivo `.env`:

### Base de Datos (PostgreSQL)

- `DATABASE_URL`: URL completa de conexión (ej: `postgresql://user:password@localhost:5432/dbname`)
- O usar variables individuales:
  - `POSTGRES_USER`: Usuario de PostgreSQL
  - `POSTGRES_PASSWORD`: Contraseña de PostgreSQL
  - `POSTGRES_SERVER`: Servidor (localhost o nombre del servicio en Docker)
  - `POSTGRES_PORT`: Puerto (por defecto 5432)
  - `POSTGRES_DB`: Nombre de la base de datos

### Aplicación

- `APP_NAME`: Nombre de la aplicación
- `SECRET_KEY`: Clave secreta para JWT (cambiar en producción)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Tiempo de expiración del token
- `CORS_ORIGINS`: Orígenes permitidos para CORS
- `DEBUG`: Modo debug (True/False)

### Lifespan

La aplicación incluye un lifespan que:
- Inicializa las tablas de la base de datos al arrancar
- Prueba la conexión a PostgreSQL antes de aceptar requests
- Cierra las conexiones correctamente al apagar la aplicación

## Desarrollo