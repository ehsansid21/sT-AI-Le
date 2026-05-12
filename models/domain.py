from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.sql import func
from core.database import Base
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    name = Column(String, nullable=True)
    # Could store preferred gender, default size, etc. here

class ClothingItem(Base):
    __tablename__ = "clothing_items"
    
    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    # For a personal app, we might not need a user_id right away, but good for future-proofing
    user_id = Column(String, nullable=True) 
    
    name = Column(String, index=True)
    category = Column(String, index=True) # e.g., Top, Bottom, Outerwear, Shoes
    color = Column(String, index=True)
    image_path = Column(String, nullable=True) # Path to the saved image file
    vector_id = Column(String, nullable=True, unique=True) # ID used in ChromaDB
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class OutfitFeedback(Base):
    __tablename__ = "outfit_feedback"
    
    id = Column(Integer, primary_key=True, index=True)
    # Storing the components that were suggested (could be JSON or comma separated IDs)
    suggested_items_ids = Column(String) 
    liked = Column(Boolean)
    weather_context = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
