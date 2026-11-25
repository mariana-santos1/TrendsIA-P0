import os
from dotenv import load_dotenv

def carregar_configuracoes():
    """Carrega as configurações do provedor LLM."""

    load_dotenv()

    return {
        "base_url": os.getenv("LLM_API_BASE_URL"),
        "caminho": os.getenv("LLM_API_PATH", "/chat/completions"),
        "api_key": os.getenv("LLM_API_KEY"),
        "modelo": os.getenv("LLM_MODEL"),
        "max_tokens": int(os.getenv("LLM_MAX_TOKENS", "2048")),
        "timeout": float(os.getenv("LLM_TIMEOUT", "60"))
    }
