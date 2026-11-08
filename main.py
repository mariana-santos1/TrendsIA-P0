from google import genai
from dotenv import load_dotenv

load_dotenv()

#inicializa  cliente gemini
client = genai.Client()

#realiza uma solicitação ao modelo
response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents="Explique brevemente o que é LLM."
)

print(response.text)