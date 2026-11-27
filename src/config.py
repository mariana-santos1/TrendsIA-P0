import os
from dotenv import load_dotenv

def carregar_configuracoes():
    """Carrega as configurações do provedor LLM."""

    # Carrega as configurações do .env
    load_dotenv()

    # Carrega os parâmetros de conexão com LLM
    try:
        config = {
            "base_url": os.getenv("LLM_API_BASE_URL"),
            "caminho": os.getenv("LLM_API_PATH", "/chat/completions"),
            "api_key": os.getenv("LLM_API_KEY"),
            "modelo": os.getenv("LLM_MODEL"),
            "max_tokens": int(os.getenv("LLM_MAX_TOKENS", "2048")),
            "timeout": float(os.getenv("LLM_TIMEOUT", "60"))
        }

    except ValueError:
        raise ValueError(
            "Os parâmetros numéricos da configuração são inválidos."
        )

    # Verifica configurações obrigatórias
    parametros_obrigatorios = {
        "base_url": "A URL da API não foi configurada.",
        "caminho": "O caminho da API não foi configurado.",
        "api_key": "A chave da API não foi configurada.", 
        "modelo": "O modelo da API não foi configurado."
    }

    for parametro, mensagem in parametros_obrigatorios.items():
        if not config[parametro] or not config[parametro].strip():
            raise ValueError(mensagem)

    # Valida os parâmetros numéricos
    if config["max_tokens"] <= 0:
        raise ValueError("O limite de tolkens deve ser maior que zero.")
    
    if config["timeout"] <= 0:
        raise ValueError("O timeout deve ser maior que zero.")

    return config