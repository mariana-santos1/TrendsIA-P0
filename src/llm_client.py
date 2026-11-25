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
                "content": preparar_prompt()
            },
            {
                "role": "user",
                "content": anotacao
            }
        ],
        "max_tokens": config["max_tokens"]
    }

    # Realiza a requisição HTTP
    try:
        resposta = requests.post(
            url,
            headers=cabecalhos,
            json=corpo,
            timeout=config["timeout"]
        )

        # Verifica erros HTTP
        if resposta.status_code in (401, 403):
            raise RuntimeError(
                "Credencial inválida ou sem autorização para acessar a API."
            ) 

        if resposta.status_code == 404:
            raise RuntimeError(
                "Modelo ou endereço não encontrado. Verifique as configurações."
            )

        if resposta.status_code == 429:
            raise RuntimeError(
                "Limite de solicitações atingido. Tente novamente mais tarde."
            )

        if resposta.status_code == 500:
            raise RuntimeError(
                "O serviço LMM está temporariamente indisponível."
            )

        resposta.raise_for_status()

        # Extrai e processa o JSON retornado pelo modelo
        dados = resposta.json()

        conteudo = dados["choices"][0]["message"]["content"]

        # Tratamento para resposta inválida
        if not isinstance(conteudo, str) or not conteudo.strip():
            raise RuntimeError(
                "O modelo retornou uma resposta vazia ou inválida."
            )
        
        return conteudo.strip()

    # Verificação de comunicação e resposta LLM

    except requests.exceptions.Timeout:
        raise RuntimeError(
            "A solicitação excedeu o tempo limite de espera."
        )

    except requests.exceptions.ConnectionError:
        raise RuntimeError(
            "Não foi possível estabelescer conexão com o serviço de LLM"
        )

    except requests.exceptions.HTTPError:
        raise RuntimeError(
            "Ocorreu um erro na comunicação com a API."
        )

    except (requests.exceptions.JSONDecodeError, ValueError, KeyError, IndexError, TypeError):
        raise RuntimeError(
            "O serviço retornou uma resposta em formato inesperado."
        )

    except requests.exceptions.RequestException:
        raise RuntimeError(
            "Ocorreu uma falha na comunicação com o serviço de LLM."
        )