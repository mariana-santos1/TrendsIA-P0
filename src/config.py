import os
from dotenv import load_dotenv

def carregar_configuracoes():
    """Carrega as configurações do provedor LLM."""

    # Carrega as configurações do .env
    load_dotenv()

    # Tenta conexão com LLM
    try:
        config = {
            "base_url": os.getenv("LLM_API_BASE_URL"),
            "caminho": os.getenv("LLM_API_PATH", "/chat/completions"),
            "api_key": os.getenv("LLM_API_KEY"),
            "modelo": os.getenv("LLM_MODEL"),
            "max_tokens": int(os.getenv("LLM_MAX_TOKENS", "2048")),
            "timeout": float(os.getenv("LLM_TIMEOUT", "60"))
        }

    # Tratamento para valores de parâmetro inválidos
    except ValueError:
        raise ValueError(
            "Os parâmetros numéricos da configuração são inválidos."
        )

    # Verifica configurações obrigatórias
    if not config["base_url"]:
        raise ValueError("A URL da API não foi configurada.")

    if not config["caminho"]:
        raise ValueError("O caminho da API não foi configurado.")
    
    if not config["api_key"]:
        raise ValueError("A chave da API não foi configurada.")
    
    if not config["modelo"]:
        raise ValueError("O modelo da API não foi configurado.")
    
    if config["max_tokens"] <= 0:
        raise ValueError("O limite de tolkens deve ser maior que zero.")
    
    if config["timeout"] <= 0:
        raise ValueError("O timeout deve ser maior que zero.")

    return config