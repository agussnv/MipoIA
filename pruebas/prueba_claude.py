import anthropic
from dotenv import load_dotenv

load_dotenv()

cliente = anthropic.Anthropic()

respuesta = cliente.messages.create(
    model="claude-haiku-4-5",
    max_tokens=1024,
    system="Eres Mipo, un asistente de voz compacto y útil. Respondes siempre en español, de forma breve y directa",
    messages=[
        {"role": "user", "content": "Hola, ¿quién eres?"}
    ]
)

print(respuesta.content[0].text)