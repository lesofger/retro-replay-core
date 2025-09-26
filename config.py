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
    
    # WooCommerce API Settings
    WOOCOMMERCE_URL: str = os.getenv("WOOCOMMERCE_URL", "https://retro-replay.com")
    WOOCOMMERCE_CONSUMER_KEY: str = os.getenv("WOOCOMMERCE_CONSUMER_KEY", "ck_6235d3701bcf965a1e54cb5e5b517fe38e639ff2")
    WOOCOMMERCE_CONSUMER_SECRET: str = os.getenv("WOOCOMMERCE_CONSUMER_SECRET", "cs_3987474b7cfcd51ff7f9abecaa86cbbb7080fea8")

settings = Settings()
