from src.config import carregar_configuracoes
from src.llm_client import chamar_llm

def organizar_anotacao(anotacao):
    """Organiza uma anotação utilizando o modelo do LLM"""

    # Carrega as configurações
    config = carregar_configuracoes()

    # Chama o modelo e retorna o resultado
    resultado = chamar_llm(anotacao.strip(), config)

    return resultado