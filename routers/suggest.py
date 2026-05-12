from fastapi import APIRouter, Depends, Form, UploadFile, File
from sqlalchemy.orm import Session
from typing import Optional
from PIL import Image
import io

from core.database import get_db
from services.recommendation import generate_outfit_suggestion

router = APIRouter(prefix="/api", tags=["suggest"])

@router.post("/suggest-outfit")
async def suggest_outfit(
    mode: str = Form(...),
    gender: str = Form(...),
    budget: str = Form(...),
    shopping_prompt: Optional[str] = Form(None),
    region: Optional[str] = Form(None),
    venue: Optional[str] = Form(None),
    vibe: Optional[str] = Form(None),
    occasion: Optional[str] = Form(None),
    height: Optional[str] = Form(None),
    weight: Optional[str] = Form(None),
    skin_tone: Optional[str] = Form(None),
    body_type: Optional[str] = Form(None),
    lat: Optional[float] = Form(None),
    lon: Optional[float] = Form(None),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    # Process Image if uploaded
    img_data = None
    if image and image.filename:
        try:
            content = await image.read()
            img_data = Image.open(io.BytesIO(content))
        except Exception as e:
            print(f"Error processing image: {e}")

    suggestion = await generate_outfit_suggestion(
        db=db,
        mode=mode,
        gender=gender,
        budget=budget,
        shopping_prompt=shopping_prompt,
        region=region,
        venue=venue,
        vibe=vibe,
        occasion=occasion,
        height=height,
        weight=weight,
        skin_tone=skin_tone,
        body_type=body_type,
        lat=lat,
        lon=lon,
        uploaded_image=img_data
    )
    
    return {"suggestion": suggestion}
