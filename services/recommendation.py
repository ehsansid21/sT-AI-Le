import google.generativeai as genai
from core.config import settings
from services.weather import get_weather
from sqlalchemy.orm import Session
from models.domain import ClothingItem
from core.vector_db import get_vector_db
import json
from PIL import Image

def init_gemini():
    if settings.GEMINI_API_KEY:
        genai.configure(api_key=settings.GEMINI_API_KEY)

async def generate_outfit_suggestion(
    db: Session,
    mode: str,
    gender: str,
    budget: str,
    shopping_prompt: str = None,
    region: str = None,
    venue: str = None,
    vibe: str = None,
    occasion: str = None,
    height: str = None,
    weight: str = None,
    skin_tone: str = None,
    body_type: str = None,
    lat: float = None,
    lon: float = None,
    styling_prompt: str = None,
    uploaded_image: Image.Image = None
):
    init_gemini()
    
    # 1. Get Weather
    weather_desc = "Unknown"
    temperature = "Unknown"
    if lat is not None and lon is not None:
        weather_desc, temperature = await get_weather(lat, lon)
        
    # 2. Get Wardrobe Context
    wardrobe_items = db.query(ClothingItem).all()
    wardrobe_context = ""
    if wardrobe_items:
        items_desc = [f"- {item.name} ({item.color} {item.category})" for item in wardrobe_items]
        wardrobe_context = "\n    **My Digital Wardrobe:**\n    " + "\n    ".join(items_desc)
        
    # 3. Vector Similarity (If Image Uploaded)
    similar_items_context = ""
    if uploaded_image:
        try:
            from services.image_processing import generate_embedding
            query_embedding = generate_embedding(uploaded_image)
            collection = get_vector_db()
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=3
            )
            if results and results['metadatas'] and len(results['metadatas'][0]) > 0:
                similar_items_desc = [f"- {meta['name']} ({meta['color']} {meta['category']})" for meta in results['metadatas'][0]]
                similar_items_context = "\n    **Similar Items in Wardrobe:**\n    " + "\n    ".join(similar_items_desc)
        except Exception as e:
            print(f"Error in vector search: {e}")

    # 4. Build Prompt
    attr_context = ""
    if height or weight or skin_tone or body_type:
        attr_context = f"\n    - Physical Attributes: Height: {height or 'N/A'}, Weight: {weight or 'N/A'}, Skin Tone: {skin_tone or 'N/A'}, Build: {body_type or 'N/A'}"
        
    if mode == "shopping":
        prompt = f"""
        You are a friendly and helpful personal fashion advisor.
        
        **Your Task:**
        1. **The Decision**: Analyze the request: "{shopping_prompt}". Give a clear verdict based on weather, attributes, and their existing wardrobe.
        2. **Practical Suggestions**: Provide 3 shopping suggestions.
        
        Context:
        - Gender/Style Preference: {gender}
        - Budget Range: {budget}
        - Current Weather: {weather_desc}, {temperature}{attr_context}{wardrobe_context}{similar_items_context}
        
        Please format clearly:
        - **### THE DECISION** (The verdict).
        - **### SHOPPING RECOMMENDATIONS** with 3 suggestions (Suggestion 1, 2, 3).
        - For each suggestion: What to Buy, Why it's good, How to Wear it, Where to find it, and Shop Now Links (Myntra, Flipkart, Ajio, Amazon).
        """
    else:
        prompt = f"""
        You are an advanced AI Fashion Stylist. Create an outfit from the user's wardrobe and provide an Outfit Score.
        
        Context:
        - Gender/Style Preference: {gender}
        - Venue: {venue if venue else 'Not specified'}
        - Vibe: {vibe if vibe else 'Any Style'}
        - Occasion: {occasion if occasion else 'Not specified'}
        - Current Weather: {weather_desc}, {temperature}{attr_context}{wardrobe_context}{similar_items_context}
        
        **User's Specific Request:** "{styling_prompt if styling_prompt else 'None specified. Just give me 3 great outfits.'}"
        
        **CRITICAL**: You MUST build the outfit primarily using items from "**My Digital Wardrobe**" if available. Focus heavily on fulfilling the User's Specific Request.
        
        Provide 3 distinct outfit options.
        For each option:
        - **The Look**: (Catchy name)
        - **Main Pieces**: (List top, bottom, outerwear - specify if it's from their wardrobe)
        - **Outfit Score**: (Score out of 10 based on weather, occasion, and style synergy. Explain why.)
        - **Styling Tip**: (One simple tip)
        """

    if not settings.GEMINI_API_KEY:
        return "### Gemini API Key Missing\n\nPlease add a `GEMINI_API_KEY` to your `.env` file."

    try:
        model = genai.GenerativeModel('gemini-flash-lite-latest')
        if uploaded_image:
            result = model.generate_content([prompt, uploaded_image])
        else:
            result = model.generate_content(prompt)
        return result.text
    except Exception as e:
        import traceback
        traceback.print_exc()
        return f"Error generating outfit: {str(e)}"
