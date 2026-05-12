import os
from PIL import Image
import io
import uuid
from core.vector_db import get_vector_db

# We'll load the model lazily so it doesn't block startup
_model = None

def get_clip_model():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        print("Loading CLIP model (this may take a moment on first run)...")
        # clip-ViT-B-32 is a good balance of size and performance
        _model = SentenceTransformer('clip-ViT-B-32')
    return _model

def generate_embedding(image: Image.Image) -> list[float]:
    """Generates an embedding vector for the given PIL Image."""
    model = get_clip_model()
    # sentence-transformers encode method can handle PIL images directly for CLIP models
    embedding = model.encode(image)
    return embedding.tolist()

async def process_and_store_image(image_bytes: bytes, clothing_item_id: str, name: str, category: str, color: str):
    """
    Background task to generate an embedding for an uploaded image
    and store it in ChromaDB.
    """
    try:
        # 1. Open Image
        image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        
        # 2. Generate Embedding
        embedding = generate_embedding(image)
        
        # 3. Store in ChromaDB
        collection = get_vector_db()
        collection.add(
            embeddings=[embedding],
            metadatas=[{
                "id": clothing_item_id,
                "name": name,
                "category": category,
                "color": color
            }],
            ids=[clothing_item_id]
        )
        print(f"Successfully generated and stored embedding for item {clothing_item_id}")
    except Exception as e:
        print(f"Error processing image in background: {e}")
