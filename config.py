import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # IGDB API Settings
    IGDB_CLIENT_ID: str = os.getenv("IGDB_CLIENT_ID", "")
    IGDB_CLIENT_SECRET: str = os.getenv("IGDB_CLIENT_SECRET", "")
    
    # MobyGames API Settings
    MOBYGAMES_API_KEY: str = os.getenv("MOBYGAMES_API_KEY", "")
    
    # Database Settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./game_library.db")
    
    # Server Settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))

settings = Settings()
