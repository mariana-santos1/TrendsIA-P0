import os
from dotenv import load_dotenv

def load_config():
    """Carrega as configurações do provedor LLM."""

    # Carrega as configurações do .env
    load_dotenv()

    # Carrega os parâmetros de conexão com LLM
    try:
        config = {
            "base_url": os.getenv("LLM_API_BASE_URL"),
            "path": os.getenv("LLM_API_PATH", "/chat/completions"),
            "api_key": os.getenv("LLM_API_KEY"),
            "model": os.getenv("LLM_MODEL"),
            "max_tokens": int(os.getenv("LLM_MAX_TOKENS", "2048")),
            "timeout": float(os.getenv("LLM_TIMEOUT", "60"))
        }

    except ValueError:
        raise ValueError(
            "Os parâmetros numéricos da configuração são inválidos."
        )

    # Verifica configurações obrigatórias
    required_parameters = {
        "base_url": "A URL da API não foi configurada.",
        "path": "O caminho da API não foi configurado.",
        "api_key": "A chave da API não foi configurada.",
        "model": "O modelo da API não foi configurado."
    }

    for parameter, message in required_parameters.items():
        if not config[parameter] or not config[parameter].strip():
            raise ValueError(message)

    # Valida os parâmetros numéricos
    if config["max_tokens"] <= 0:
        raise ValueError("O limite de tokens deve ser maior que zero.")

    if config["timeout"] <= 0:
        raise ValueError("O timeout deve ser maior que zero.")

    return config
