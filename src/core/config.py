from pathlib import Path
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

class Settings(BaseSettings):
    # Azure Settings
    AZURE_OPENAI_API_KEY: str = os.getenv('AZURE_OPENAI_API_KEY', '')
    AZURE_OPENAI_ENDPOINT: str = os.getenv('AZURE_OPENAI_ENDPOINT', '')
    CHAT_DEPLOYMENT: str = os.getenv('CHAT_DEPLOYMENT', 'gpt-4o')
    EMBEDDING_DEPLOYMENT: str = os.getenv('EMBEDDING_DEPLOYMENT', 'text-embeding-model')
    API_VERSION: str = os.getenv('API_VERSION', '2024-02-15-preview')
    EMBEDDING_API_VERSION: str = os.getenv('EMBEDDING_API_VERSION', '2023-05-15')
    
    # Model Settings
    CHUNK_SIZE: int = 2000
    CHUNK_OVERLAP: int = 400
    MAX_TOKENS: int = 1000
    TEMPERATURE: float = 0.1
    
    # Paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    RAW_DATA_DIR: Path = DATA_DIR / "raw"
    PROCESSED_DATA_DIR: Path = DATA_DIR / "processed"
    ASSETS_DIR: Path = BASE_DIR / "assets"
    CONFIG_DIR: Path = BASE_DIR / "config"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Crear directorios necesarios
        self.RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
        self.PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    class Config:
        env_file = ".env"

# Intentar cargar .env desde diferentes ubicaciones
possible_env_paths = [
    Path.cwd() / ".env",
    Path.cwd() / "config" / ".env",
    Path(__file__).resolve().parent.parent.parent / "config" / ".env"
]

env_file_loaded = False
for env_path in possible_env_paths:
    if env_path.exists():
        load_dotenv(str(env_path))
        env_file_loaded = True
        break

if not env_file_loaded:
    print("WARNING: No se encontró archivo .env")

settings = Settings()

# Validar configuración crítica
if not all([
    settings.AZURE_OPENAI_API_KEY,
    settings.AZURE_OPENAI_ENDPOINT,
    settings.CHAT_DEPLOYMENT,
    settings.API_VERSION
]):
    print("""
    ⚠️ Configuración incompleta. Asegúrate de tener un archivo .env con:
    AZURE_OPENAI_API_KEY=tu_api_key
    AZURE_OPENAI_ENDPOINT=tu_endpoint
    CHAT_DEPLOYMENT=nombre_deployment
    API_VERSION=version_api
    """) 