import os
from pathlib import Path
from dotenv import load_dotenv
import logging

def load_environment():
    try:
        # Configurar logging
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)

        # Obtener la ruta al directorio config
        config_dir = Path(__file__).resolve().parent.parent.parent / "config"
        env_path = config_dir / ".env"
        
        logger.info(f"Buscando archivo .env en: {env_path}")
        
        # Cargar variables de entorno
        if env_path.exists():
            load_dotenv(env_path)
            
            # Verificar variables críticas
            required_vars = [
                'AZURE_OPENAI_API_KEY',
                'AZURE_OPENAI_ENDPOINT',
                'AZURE_OPENAI_DEPLOYMENT',
                'AZURE_EMBEDDING_DEPLOYMENT',
                'AZURE_API_VERSION',
                'AZURE_EMBEDDING_API_VERSION'
            ]
            
            # Imprimir valores para debug
            for var in required_vars:
                value = os.getenv(var)
                logger.info(f"{var}: {'✓ Configurado' if value else '✗ No encontrado'}")
            
            return True
        else:
            logger.error(f"Archivo .env no encontrado en {env_path}")
            return False
    except Exception as e:
        logger.error(f"Error cargando variables de entorno: {e}")
        return False 