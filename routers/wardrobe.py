from fastapi import APIRouter, Depends, UploadFile, File, Form, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
import shutil
import os

from core.database import get_db
from models.domain import ClothingItem
from services import wardrobe as wardrobe_service
from services.image_processing import process_and_store_image

router = APIRouter(prefix="/api/wardrobe", tags=["wardrobe"])

# Ensure uploads directory exists
UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/add")
async def add_item(
    background_tasks: BackgroundTasks,
    name: str = Form(...),
    category: str = Form(...),
    color: str = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # 1. Save image locally (or to cloud storage in production)
    file_path = os.path.join(UPLOAD_DIR, image.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
        
    # 2. Add to SQL Database
    db_item = wardrobe_service.create_clothing_item(db, name, category, color, file_path)
    
    # 3. Read image bytes for background processing
    with open(file_path, "rb") as f:
        image_bytes = f.read()
        
    # 4. Trigger Background Task for embedding
    background_tasks.add_task(
        process_and_store_image,
        image_bytes,
        db_item.id,
        name,
        category,
        color
    )
    
    return {"message": "Item added to wardrobe and processing started", "item_id": db_item.id}

@router.get("/items")
def get_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = wardrobe_service.get_clothing_items(db, skip=skip, limit=limit)
    return items

@router.delete("/{item_id}")
def delete_item(item_id: str, db: Session = Depends(get_db)):
    deleted = wardrobe_service.delete_clothing_item(db, item_id)
    if deleted:
        return {"message": "Item deleted"}
    return {"message": "Item not found"}, 404
