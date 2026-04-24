from fastapi import FastAPI, Form, UploadFile, File, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import httpx
import os
import google.generativeai as genai
from dotenv import load_dotenv
from typing import Optional
from PIL import Image
import io

load_dotenv(override=True)

app = FastAPI()

# Configure Gemini
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# Mount static files for the frontend
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_root():
    return {"message": "Visit /static/index.html to see the frontend."}

@app.post("/api/suggest-outfit")
async def suggest_outfit(
    mode: str = Form(...),
    gender: str = Form(...),
    budget: str = Form(...),
    shopping_prompt: Optional[str] = Form(None),
    region: Optional[str] = Form(None),
    venue: Optional[str] = Form(None),
    vibe: Optional[str] = Form(None),
    occasion: Optional[str] = Form(None),
    available_clothes: Optional[str] = Form(None),
    height: Optional[str] = Form(None),
    weight: Optional[str] = Form(None),
    skin_tone: Optional[str] = Form(None),
    body_type: Optional[str] = Form(None),
    lat: Optional[float] = Form(None),
    lon: Optional[float] = Form(None),
    image: Optional[UploadFile] = File(None)
):
    # Fetch weather using Open-Meteo
    weather_desc = "Unknown"
    temperature = "Unknown"
    
    if lat is not None and lon is not None:
        async with httpx.AsyncClient() as client:
            url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
            try:
                response = await client.get(url)
                if response.status_code == 200:
                    weather_data = response.json().get("current_weather", {})
                    temp_c = weather_data.get("temperature")
                    weather_code = weather_data.get("weathercode")
                    temperature = f"{temp_c}°C"
                    if weather_code < 3:
                        weather_desc = "Clear/Sunny"
                    elif weather_code < 50:
                        weather_desc = "Cloudy/Foggy"
                    elif weather_code < 70:
                        weather_desc = "Rainy"
                    else:
                        weather_desc = "Snowy"
            except Exception as e:
                print(f"Weather error: {e}")

    # Process Image if uploaded
    img_data = None
    if image and image.filename:
        try:
            content = await image.read()
            img_data = Image.open(io.BytesIO(content))
        except Exception as e:
            print(f"Error processing image: {e}")

    # Construct the Prompt
    clothes_context = f"\n    - Available Clothes: {available_clothes}" if available_clothes else ""
    attr_context = ""
    if height or weight or skin_tone or body_type:
        attr_context = f"\n    - Physical Attributes: Height: {height or 'N/A'}, Weight: {weight or 'N/A'}, Skin Tone: {skin_tone or 'N/A'}, Build: {body_type or 'N/A'}"
    
    if mode == "shopping":
        prompt = f"""
        You are a friendly and helpful personal fashion advisor.
        
        **Your Task:**
        1. **The Decision**: First, analyze the user's specific request: "{shopping_prompt}". If they are confused between multiple items or colors (e.g., beige vs. charcoal), give a clear "General Statement" deciding which one is better for them and why. Consider their physical attributes and the current weather in your reasoning.
        2. **Practical Suggestions**: After the decision, provide 3 specific shopping suggestions that align with that choice.
        
        Context:
        - Gender/Style Preference: {gender}
        - Budget Range: {budget}
        - Current Weather: {weather_desc}, {temperature}{attr_context}
        
        Please format your response clearly:
        - Start with a section called **### THE DECISION** (The general statement/verdict).
        - Followed by **### SHOPPING RECOMMENDATIONS** with 3 suggestions (Suggestion 1, 2, 3).
        
        For each suggestion, list:
        - **What to Buy:** (A simple description)
        - **Why it's good for you:** (Based on their needs and attributes)
        - **How to Wear it:** (A quick styling tip)
        - **Where to find it:** (Brands matching the {budget} budget)
        - **Shop Now (Links):** Search links for:
          - [Myntra](https://www.myntra.com/search?q=[ITEM_NAME])
          - [Flipkart](https://www.flipkart.com/search?q=[ITEM_NAME])
          - [Ajio](https://www.ajio.com/search/?text=[ITEM_NAME])
          - [Amazon](https://www.amazon.in/s?k=[ITEM_NAME])
        """
    else:
        prompt = f"""
        You are a friendly and practical fashion stylist. The user needs a simple outfit idea for today.
        
        Context:
        - Gender/Style Preference: {gender}
        - Budget Range: {budget}
        - Region / Location: {region or 'Not specified'}
        - Venue: {venue}
        - Vibe: {vibe}
        - Occasion: {occasion}
        - Current Weather: {weather_desc}, {temperature}{clothes_context}{attr_context}
        
        Please provide 3 distinct outfit options formatted as **Option 1**, **Option 2**, and **Option 3**.
        Use simple language and avoid fashion jargon. Use bullet points.
        
        For each option, quickly list:
        - **The Look:** (A short, catchy name for the outfit)
        - **Main Pieces:** (List the top, bottom, and any jacket or outer layer)
        - **Shoes & Accessories:** (What shoes and maybe a watch or bag to wear)
        - **Styling Tip:** (One simple tip to make the outfit look better, like "tuck in the shirt" or "roll up the sleeves")
        
        Make sure the clothes suggested are common items that most people can easily find in a regular store or already have in their closet.
        """
        if available_clothes:
            prompt += "\n\nCRITICAL: You MUST incorporate the user's 'Available Clothes' into your suggestions as much as possible."

    if not api_key:
        return JSONResponse({
            "suggestion": "### Gemini API Key Missing\n\nPlease add a `GEMINI_API_KEY` to your `.env` file."
        })

    try:
        model = genai.GenerativeModel('gemini-flash-lite-latest')
        
        if img_data:
            result = model.generate_content([prompt, img_data])
        else:
            result = model.generate_content(prompt)
            
        return JSONResponse({"suggestion": result.text})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse({"suggestion": f"Error generating outfit: {str(e)}"}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
