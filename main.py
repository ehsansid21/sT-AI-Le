from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv

from core.database import engine, Base
from routers import wardrobe, suggest, feedback

# Load environment variables
load_dotenv(override=True)

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Personal Fashion Assistant")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include Routers
app.include_router(wardrobe.router)
app.include_router(suggest.router)
app.include_router(feedback.router)

@app.get("/")
async def read_root():
    return RedirectResponse(url="/static/index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
