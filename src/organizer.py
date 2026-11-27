from src.config import load_config
from src.llm_client import call_llm

def organize_note(note):
    """Organiza uma anotação utilizando o modelo do LLM"""

    # Valida a entrada
    if not note or not note.strip():
        raise ValueError("A anotação não pode estar vazia.")

    # Carrega as configurações
    config = load_config()

    # Chama o modelo e retorna o resultado
    result = call_llm(note.strip(), config)

    return result