import tiktoken
from typing import Dict

class TokenCounter:
    def __init__(self, model_name: str = "gpt-4"):
        """
        Inicializa el contador de tokens.
        Args:
            model_name (str): Nombre del modelo para el encoding
        """
        self.encoding = tiktoken.encoding_for_model(model_name)
        self.total_tokens = 0
        self.cost_per_1k = 0.03  # $0.03 por 1000 tokens
    
    def count_tokens(self, text: str) -> int:
        """
        Cuenta tokens en un texto.
        Args:
            text (str): Texto a analizar
        Returns:
            int: Número de tokens
        """
        if not text:
            return 0
        return len(self.encoding.encode(text))
    
    def update_total(self, tokens: int):
        """
        Actualiza el contador total de tokens.
        Args:
            tokens (int): Número de tokens a añadir
        """
        self.total_tokens += tokens
    
    def calculate_cost(self, tokens: int) -> float:
        """
        Calcula el costo para un número de tokens.
        Args:
            tokens (int): Número de tokens
        Returns:
            float: Costo en dólares
        """
        return (tokens / 1000) * self.cost_per_1k
    
    def get_metrics(self) -> Dict:
        """
        Retorna métricas actuales.
        Returns:
            Dict: Diccionario con total de tokens y costo
        """
        return {
            "total_tokens": self.total_tokens,
            "total_cost": self.calculate_cost(self.total_tokens)
        }
    
    def reset(self):
        """Reinicia el contador de tokens"""
        self.total_tokens = 0 