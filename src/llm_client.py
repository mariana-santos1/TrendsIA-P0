import requests

from src.prompt import preparar_prompt

def chamar_llm(anotacao, config):
    """Envia a solicitação ao LLM e retorna a resposta."""

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
                "content": anotacao
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
