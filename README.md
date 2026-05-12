# 👗 AI Personal Fashion Assistant

An advanced AI-powered web application that acts as your personal stylist and shopper. Built with **FastAPI**, **Google Gemini AI**, **ChromaDB**, and **SQLite**.

## ✨ Features

- **Digital Wardrobe Database**: Upload and manage your clothing items. Your items are stored locally in an SQLite database.
- **Visual Similarity Search**: Uses `clip-ViT-B-32` AI embeddings and **ChromaDB** to "see" your clothes and find visually similar items.
- **Smart Outfit Recommendation Engine**: The AI actively pulls from your Digital Wardrobe to create outfits and provides an "Outfit Score" based on synergy, occasion, and current weather.
- **Background Image Processing**: Image embeddings are generated asynchronously using FastAPI Background Tasks, keeping the UI lightning fast.
- **Dual-Mode Experience**:
  - **Outfit Stylist**: Get instant outfit recommendations tailored to you.
  - **Shopping Advice**: Personalized shopping suggestions based on your body type, skin tone, and existing wardrobe.
- **Real-time Weather Integration**: Automatically fetches local weather to ensure your outfit is practical.
- **E-commerce Ready**: Generates direct search links for Myntra, Flipkart, Ajio, and Amazon for all shopping recommendations.

## 🛠️ Tech Stack

- **Backend Architecture**: Modular FastAPI (Routers, Services, Core)
- **Relational Database**: SQLite via SQLAlchemy
- **Vector Database**: ChromaDB
- **Embedding Model**: `sentence-transformers` (`clip-ViT-B-32`)
- **LLM Engine**: Google Gemini AI (`gemini-flash-lite-latest`)
- **Frontend**: Vanilla HTML5, CSS3, and JavaScript (Glassmorphism UI)
- **APIs**: Open-Meteo (Weather Data), Geolocation API

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.8+
- A Google Gemini API Key ([Get one here](https://aistudio.google.com/app/apikey))

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/ehsansid21/sT-AI-Le.git
cd sT-AI-Le/ai-outfit-suggester

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies (Note: The first time you run the app, it will download the CLIP model ~500MB)
pip install -r requirements.txt
```

### 3. Configuration
Create a `.env` file in the root directory (`ai-outfit-suggester/`) and add your API key:
```env
GEMINI_API_KEY=your_actual_api_key_here
```

### 4. Running the App
```bash
uvicorn main:app --port 8001 --reload
```
Open your browser and visit: `http://127.0.0.1:8001/` (The root endpoint will guide you to the static UI at `/static/index.html`).

## 💡 Note on First Run
The first time you upload an item with a photo to your Digital Wardrobe, the backend will download the `clip-ViT-B-32` model in the background to generate the vector embeddings. This might take a minute depending on your internet connection. Subsequent uploads will be nearly instantaneous.

## 📄 License
MIT License
