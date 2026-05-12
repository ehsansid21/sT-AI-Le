import httpx
from typing import Tuple

async def get_weather(lat: float, lon: float) -> Tuple[str, str]:
    """
    Fetches the current weather description and temperature.
    Returns: (weather_desc, temperature_string)
    """
    weather_desc = "Unknown"
    temperature = "Unknown"
    
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
            
    return weather_desc, temperature
