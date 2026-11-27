import requests

from src.prompt import build_prompt

def call_llm(note, config):
    """Envia a solicitação ao LLM e retorna a resposta."""

    # Monta o endereço da requisição
    url = (
        config["base_url"].rstrip("/")
        + "/"
        + config["path"].lstrip("/")
    )

    # Configura a autenticação
    headers = {
        "Authorization": f"Bearer {config['api_key']}"
    }

    # Monta o conteúdo enviado ao modelo
    payload = {
        "model": config["model"],
        "messages": [
            {
                "role": "system",
                "content": build_prompt()
            },
            {
                "role": "user",
                "content": note
            }
        ],
        "max_tokens": config["max_tokens"]
    }

    # Realiza a requisição HTTP
    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=config["timeout"]
        )

        # Verifica erros HTTP
        if response.status_code == 401:
            raise RuntimeError(
                "Credencial inválida ou não reconhecida pelo serviço."
            )

        if response.status_code == 403:
            raise RuntimeError(
                "Acesso não autorizado. Verifique as permissões da credencial."
            )

        if response.status_code == 404:
            raise RuntimeError(
                "Modelo ou endereço não encontrado. Verifique as configurações."
            )

        if response.status_code == 429:
            raise RuntimeError(
                "Limite de solicitações atingido. Tente novamente mais tarde."
            )

        if response.status_code == 503:
            raise RuntimeError(
                "O modelo está temporariamente sobrecarregado. Tente novamente em alguns instantes."
            )

        if response.status_code >= 500:
            raise RuntimeError(
                "O serviço do LLM está temporariamente indisponível."
            )

        response.raise_for_status()

        # Extrai e processa o JSON retornado pelo modelo
        data = response.json()

        content = data["choices"][0]["message"]["content"]

        # Tratamento para resposta inválida
        if not isinstance(content, str) or not content.strip():
            raise RuntimeError(
                "O modelo retornou uma resposta vazia ou inválida."
            )
        
        return content.strip()

    # Verificação de comunicação e resposta LLM

    except requests.exceptions.Timeout:
        raise RuntimeError(
            "A solicitação excedeu o tempo limite de espera."
        )

    except requests.exceptions.ConnectionError:
        raise RuntimeError(
            "Não foi possível estabelecer conexão com o serviço de LLM"
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