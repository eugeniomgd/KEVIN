import logging
from pathlib import Path
from datetime import datetime
from .config import settings

class Logger:
    def __init__(self, name: str = "KEVIN"):
        self.logger = logging.getLogger(name)
        if not self.logger.handlers:
            self._setup_logger()
    
    def _setup_logger(self):
        self.logger.setLevel(logging.INFO)
        
        # Configurar formato
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Handler para consola
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # Handler para archivo
        log_dir = settings.BASE_DIR / "logs"
        log_dir.mkdir(exist_ok=True)
        
        file_handler = logging.FileHandler(
            log_dir / f"app_{datetime.now().strftime('%Y%m%d')}.log"
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
    
    def info(self, message: str):
        self.logger.info(message)
    
    def error(self, message: str):
        self.logger.error(message)
    
    def warning(self, message: str):
        self.logger.warning(message) 