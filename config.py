import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    serpapi_api_key: str = os.getenv("SERPAPI_API_KEY", "")
    serpapi_location: str = os.getenv("SERPAPI_LOCATION", "India")
    serpapi_hl: str = os.getenv("SERPAPI_HL", "en")
    serpapi_gl: str = os.getenv("SERPAPI_GL", "in")
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
    cache_ttl_seconds: int = int(os.getenv("CACHE_TTL_SECONDS", "300"))
    db_path: str = os.getenv("SHOPPING_DB_PATH", "data/shopping.db")

settings = Settings()
