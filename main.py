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
        "temperatura": float(os.getenv("LLM_TEMPERATURE", "0.7")),
        "max_tokens": int(os.getenv("LLM_MAX_TOKENS", "1000")),
        "timeout": float(os.getenv("LLM_TIMEOUT", "30"))
    }

def organizar_anotacao(anotacao):
    """Envia a anotação ao LLM e retorna a lista organizada."""
    
    config = carregar_configuracoes()

    prompt = """
    Você é um assistente responsável por organizar anotações.
    Sua tarefa é transformar o texto fornecido pelo usuário em uma lista clara e organizada de tarefas. 

    Instruções:
    - identifique todas as tarefas mencionadas;
    - organize as tarefas em uma lista numerada;
    - identifique os prazos quando estiverem presentes;
    - identifique os responsáveis quando estiverem presentes;
    - não invente informações que não estejam no texto;
    - quando não houver prazo, informe "Prazo não definido.";
    - quando o responsável for o próprio usuário, informe "Eu";
    - utilize uma linguagem clara e objetiva;
    - utilize uma formatação de texto simples e limpa, sem markdown.
    """

    # monta o endereço da requisição
    url = (
        config["base_url"].rstrip("/")
        + "/"
        + config["caminho"].lstrip("/")
    )

    # configura a autenticação
    cabecalhos = {
        "Authorization": f"Bearer {config['api_key']}"
    }

    # monta o conteúdo enviado ao modelo
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
        "temperature": config["temperatura"],
        "max_tokens": config["max_tokens"]
    }

    # realiza a requisição HTTP
    resposta = requests.post(
        url,
        headers=cabecalhos,
        json=corpo,
        timeout=config["timeout"]
    )

    resposta.raise_for_status()

    # extrai o texto retornado pelo modelo
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
