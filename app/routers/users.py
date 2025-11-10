"""
Router para endpoints de usuarios
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas import user as user_schema
from app.services import user_service as user_service_module
from app.core.security import create_access_token
from datetime import timedelta
from app.core.config import settings

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=user_schema.User, status_code=status.HTTP_201_CREATED)
def create_user(
    user: user_schema.UserCreate,
    db: Session = Depends(get_db)
):
    """Crea un nuevo usuario"""
    # Verificar si el usuario ya existe
    db_user = user_service_module.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )
    
    db_user = user_service_module.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El username ya está en uso"
        )
    
    return user_service_module.create_user(db=db, user=user)


@router.get("/", response_model=List[user_schema.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtiene una lista de usuarios"""
    users = user_service_module.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=user_schema.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """Obtiene un usuario por ID"""
    db_user = user_service_module.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return db_user


@router.put("/{user_id}", response_model=user_schema.User)
def update_user(
    user_id: int,
    user_update: user_schema.UserUpdate,
    db: Session = Depends(get_db)
):
    """Actualiza un usuario"""
    db_user = user_service_module.update_user(db, user_id, user_update)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return db_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Elimina un usuario"""
    success = user_service_module.delete_user(db, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )


@router.post("/login", response_model=user_schema.Token)
def login(user_credentials: user_schema.UserLogin, db: Session = Depends(get_db)):
    """Autentica un usuario y devuelve un token JWT"""
    user = user_service_module.authenticate_user(
        db, user_credentials.username, user_credentials.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

