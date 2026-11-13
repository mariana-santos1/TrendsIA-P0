import os
import requests
from dotenv import load_dotenv

load_dotenv()

def carregar_configuracoes():
    """Carrega as configurações do provedor LLM."""

    return {
        "base_url": os.getenv("LLM_API_BASE_URL"),
        "caminho": os.getenv("LLM_API_PATH", "/chat/completions"),
        "api_key": os.getenv("LLM_API_KEY"),
        "modelo": os.getenv("LLM_MODEL"),
        "max_tokens": int(os.getenv("LLM_MAX_TOKENS", "2048")),
        "timeout": float(os.getenv("LLM_TIMEOUT", "60"))
    }

def organizar_anotacao(anotacao):
    """Envia a anotação ao LLM e retorna a lista organizada."""
    
    config = carregar_configuracoes()

    prompt = """
    Você é um assistente especializado em identificar e organizar tarefas presentes em anotações escritas em linguagem natural. Sua tarefa é extrair todas as tarefas mencionadas pelo usuário e apresentá-las em uma lista numerada.

    Instruções:
    - Identifique todas as tarefas, sem deixar nenhuma de fora.
    - Identifique os prazos mencionados no texto.
    - Quando não houver prazo identificado, informe "Não definido".  
    - Não invente informações.
    - Utilize uma formatação de texto simples e limpa, sem markdown.

    Formato obrigatório da resposta:
    1. Tarefa: [descrição da tarefa]
       Prazo: [prazo ou Não definido]

    2. Tarefa: [descrição da tarefa]
       Prazo: [prazo ou Não definido]
    """

    # Monta o endereço da requisição
    url = (
        config["base_url"].rstrip("/")
        + "/"
        + config["caminho"].lstrip("/")
    )

    # Configura a autenticação
    cabecalhos = {
        "Authorization": f"Bearer {config['api_key']}"
    }

    # Monta o conteúdo enviado ao modelo
    corpo = {
        "model": config["modelo"],
        "messages": [
            {
                "role": "system",
                "content": prompt
            },
            {
                "role": "user",
                "content": anotacao
            }
        ],
        "max_tokens": config["max_tokens"]
    }

    # Realiza a requisição HTTP
    resposta = requests.post(
        url,
        headers=cabecalhos,
        json=corpo,
        timeout=config["timeout"]
    )

    resposta.raise_for_status()

    # Extrai o texto retornado pelo modelo
    dados = resposta.json()

    return dados["choices"][0]["message"]["content"]

def main():
    print("Oganizador de Anotações")

    anotacao = input("\nDigite sua anotação:\n")

    if not anotacao:
        print("\nErro: a anotação não pode estar vazia!")
        return

    resultado = organizar_anotacao(anotacao)

    print("\nAnotação Organizada:")
    print(resultado)

if __name__ == "__main__":
    main()
