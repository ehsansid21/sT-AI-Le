# 👗 AI Fashion Assistant

An AI-powered web application that acts as your personal stylist and shopper. Built with **FastAPI**, **Google Gemini AI**, and **Open-Meteo API**.

## ✨ Features

- **Dual-Mode Experience**:
  - **Outfit Stylist**: Get instant outfit recommendations based on the current local weather and your existing wardrobe.
  - **Shopping Advice**: Personalized shopping suggestions based on your body type, skin tone, and specific fashion goals.
- **Multimodal AI**: Upload photos of your clothes for the AI to analyze and style around.
- **Real-time Weather Integration**: Automatically fetches local weather to ensure your outfit is practical.
- **E-commerce Ready**: Generates direct search links for Myntra, Flipkart, Ajio, and Amazon for all shopping recommendations.
- **Accessibility**: Practical, friendly advice focused on common, affordable brands.

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python)
- **AI Engine**: Google Gemini AI (`gemini-flash-lite-latest`)
- **Frontend**: Vanilla HTML5, CSS3, and JavaScript
- **APIs**: Open-Meteo (Weather Data), Geolocation API

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.8+
- A Google Gemini API Key ([Get one here](https://aistudio.google.com/app/apikey))

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/ehsansid21/sT-AI-Le.git
cd sT-AI-Le

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration
Create a `.env` file in the root directory and add your API key:
```env
GEMINI_API_KEY=your_actual_api_key_here
```

### 4. Running the App
```bash
uvicorn main:app --reload
```
Open your browser and visit: `http://127.0.0.1:8000/static/index.html`

## 📸 Screenshots
*(Add your screenshots here)*

## 📄 License
MIT License
