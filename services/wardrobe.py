from sqlalchemy.orm import Session
from models.domain import ClothingItem
import uuid
from typing import List

def create_clothing_item(db: Session, name: str, category: str, color: str, image_path: str = None) -> ClothingItem:
    item_id = str(uuid.uuid4())
    db_item = ClothingItem(
        id=item_id,
        name=name,
        category=category,
        color=color,
        image_path=image_path,
        vector_id=item_id
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_clothing_items(db: Session, skip: int = 0, limit: int = 100) -> List[ClothingItem]:
    return db.query(ClothingItem).offset(skip).limit(limit).all()

def delete_clothing_item(db: Session, item_id: str):
    db_item = db.query(ClothingItem).filter(ClothingItem.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item
