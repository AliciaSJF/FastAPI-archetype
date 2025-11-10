"""
Servicio de lógica de negocio para items
"""
from sqlalchemy.orm import Session
from typing import Optional, List
from app.db import models
from app.schemas import item as item_schema


def get_item(db: Session, item_id: int) -> Optional[models.Item]:
    """Obtiene un item por ID"""
    return db.query(models.Item).filter(models.Item.id == item_id).first()


def get_items(db: Session, skip: int = 0, limit: int = 100, owner_id: Optional[int] = None) -> List[models.Item]:
    """Obtiene una lista de items"""
    query = db.query(models.Item)
    if owner_id:
        query = query.filter(models.Item.owner_id == owner_id)
    return query.offset(skip).limit(limit).all()


def create_item(db: Session, item: item_schema.ItemCreate, owner_id: int) -> models.Item:
    """Crea un nuevo item"""
    db_item = models.Item(**item.model_dump(), owner_id=owner_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_item(db: Session, item_id: int, item_update: item_schema.ItemUpdate) -> Optional[models.Item]:
    """Actualiza un item"""
    db_item = get_item(db, item_id)
    if not db_item:
        return None
    
    update_data = item_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_item, field, value)
    
    db.commit()
    db.refresh(db_item)
    return db_item


def delete_item(db: Session, item_id: int) -> bool:
    """Elimina un item"""
    db_item = get_item(db, item_id)
    if not db_item:
        return False
    
    db.delete(db_item)
    db.commit()
    return True

