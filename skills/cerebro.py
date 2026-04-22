import json
import anthropic
from dotenv import load_dotenv

load_dotenv()

cliente = anthropic.Anthropic()

PERSONALIDAD = """
Eres Mipo, un asistente de voz compacto y portátil.
Respondes siempre en español (a menos que te hablen en otro idioma), de forma breve y directa.
MÁXIMO 2-3 frases por response - eres un asistente de voz, no un ensayista. Pero si te hacen una pregunta, responde de la forma más breve posible.
Bajo ningún concepto, utilices emojis.
Si no entiendes algo, pides aclaración en una sola frase.
Puedes ayudar con cualquier tema: programación, electrónica, cocina, matemáticas, o lo que sea que el usuario necesite.
"""

HERRAMIENTAS = [
    {
        "name": "temporizador",
        "description": "Inicia un temporizador. Úsalo cuando el usuario quiera poner un timer, cuenta atrás o que le avises en X tiempo",
        "input_schema": {
            "type": "object",
            "properties": {
                "segundos": { "type": "integer", "description": "Duración del temporizador en segundos" }
            },
            "required": ["segundos"]
        },
    },
    {
        "name": "guardar_nota",
        "description": "Guarda una nota. Úsalo cuando el usuario quiera guardar una nota, un recordatorio o apuntar alguna cosa",
        "input_schema": {
            "type": "object",
            "properties": {
                "text": { "type": "string", "description": "El text EXACTO de la nota que debe guardar" }
            },
            "required": ["text"]
        }
    },
    {
        "name": "ver_notas",
        "description": "Muestra todas las notas guardadas. Úsala cuando el usuario quiera ver todas las notas guardadas, todos los recordatorios, leer o consultar sus notas",
        "input_schema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "ver_historial",
        "description": "Muestra todo el historial de mensajes que tuvo el usuario. Úsalo cuando el usuario quiera ver el historial de mensajes o comandos anteriores",
        "input_schema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "consultar_bateria",
        "description": "Muestra la cantidad de batería. Úsala cuando el usuario quiera consultar la batería o energía de Mipo.",
        "input_schema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "enviar_mail",
        "description":
        """
        Envía un mail. Úsala cuando el usuario quiera enviar un correo electrónico. IMPORTANTE: antes de ejecutar,
        confirma siempre el mensaje y el destinatario con el usuario, sin poner texto en negrita ni nada, solo diciendo el contenido de cada parte,
        ya que lo leerás en voz alta. Recuerda que el asunto lo debes generar tú automáticamente en base al mensaje del usuario.
        
        Para el campo recipients hay dos casos:
        - Si el usuario quiere responder a un correo leído previamente, usa el email completo del remitente que tienes en el historial de conversación.
        - Si el usuario quiere enviar a un contacto de su agenda, pasa el nombre tal como lo diga el usuario y Python lo resolverá automáticamente.
        """,
        "input_schema": {
            "type": "object",
            "properties": {
                "recipients": { "type": "string", "description": "Dirección o direcciones de email destinatarias" },
                "body": { "type": "string", "description": "El mensaje que el usuario quiere enviar." },
                "subject": { "type": "string", "description": "Asunto del mail, generado automáticamente a partir del body." }
            },
            "required": ["recipients", "body", "subject"]
        }
    },
    {
        "name": "ver_correos",
        "description": "Obtiene y resume los correos recibidos hoy según el asunto. Úsala cuando el usuario quiera saber qué emails ha recibido hoy, cuántos correos tiene, un resumen de su bandeja de entrada o qué le han escrito.",
        "input_schema": {
            "type": "object",
            "properties": {}
        }
    }
]

historial_conversacion = []

def preguntar(mensaje_usuario):
    historial_conversacion.append({
        "role":"user",
        "content": mensaje_usuario
    })
    
    # if len(historial_conversacion) > 20:
    #     historial_conversacion = historial_conversacion[-10:]

    response = cliente.messages.create(
        model="claude-haiku-4-5",
        max_tokens=1024,
        system=PERSONALIDAD,
        tools=HERRAMIENTAS,
        messages=historial_conversacion
    )

    if response.stop_reason == "tool_use":
        for content in response.content:
            if content.type == "tool_use":

                # Guardamos la respuesta de Claude donde define la herramienta
                historial_conversacion.append({
                    "role": "assistant",
                    "content": response.content
                })

                # Informamos a Claude del resultado (tool_result)
                historial_conversacion.append({
                    "role": "user",
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": content.id,
                            "content": "Hecho."
                        }
                    ]
                })
                return {"tipo": "herramienta", "nombre": content.name, "params": content.input}
    
    text = response.content[0].text
    historial_conversacion.append({
        "role":"assistant",
        "content": text
    })

    return {"tipo": "texto", "contenido": text}