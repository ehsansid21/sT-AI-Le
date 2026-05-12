from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    GEMINI_API_KEY: str = ""
    SQLITE_URL: str = "sqlite:///./wardrobe.db"
    CHROMA_DB_DIR: str = "./chroma_db"
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
