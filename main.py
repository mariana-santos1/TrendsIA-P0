from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client()

def organizar_anotacao(anotacao):
    prompt = f"""
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
    - utilize uma formatação de texto simples e limpa.

    Anotação do usuário:
    {anotacao} 
    """

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt 
    )

    return response.text

def main():
    print("Oganizador de Anotações")

    anotacao = input("\nDigite sua anotação:\n")

    resultado = organizar_anotacao(anotacao)

    print("\nAnotação Organizada")
    print(resultado)

if __name__ == "__main__":
    main()
