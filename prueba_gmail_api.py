import base64
import os.path
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from requests import HTTPError
from datetime import datetime
import emoji

ARCHIVO = "credentials.json"

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly"
]

def obtener_cuerpo(payload):
    if "parts" in payload: # Cuando el correo tiene diferentes tipos de datos adjuntos: texto plano, código HTML, imágenes, etc. Recorre cada una de ellas buscando el texto.
        for part in payload["parts"]:
            if part["mimeType"] == "text/plain": # Buscamos el texto, pero también podemos buscar text/html (versión HTML), image/jpeg || image/png, application/pdf, multipart/mixed (varias partes), multipart/alternative (cuando el mismo mensaje tiene texto y html juntos)
                data = part["body"].get("data", "") # Si
                return base64.urlsafe_b64decode(data).decode("utf-8")
    elif "body" in payload: # Cuando el correo solo trae texto plano.
        data = payload["body"].get("data", "")
        if data:
            return base64.urlsafe_b64decode(data).decode("utf-8")
    return "Sin contenido"

def autenticar():
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(ARCHIVO, SCOPES)
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)

def obtener_correos_hoy():
    service = autenticar()
    try:
        today = datetime.now().strftime("%Y/%m/%d")
        results = (
            service.users().messages().list(userId="me", labelIds=["INBOX"], q=f"after:{today}").execute()
        )
        messages = results.get("messages", [])
        if not messages:
            return "No tienes correos nuevos hoy."
        
        resumenes = []
        for message in messages:
            msg = (
                service.users().messages().get(
                    userId="me",
                    id=message["id"],
                    format="full"
                ).execute()
            )
            
            headers = msg["payload"]["headers"]
            asunto = next((h["value"] for h in headers if h["name"] == "Subject"), "Sin asunto")
            remitente = next((h["value"] for h in headers if h["name"] == "From"), "Desconocido")
            cuerpo = obtener_cuerpo(msg["payload"])
            
            if cuerpo.startswith("<!DOCTYPE html>"):
                cuerpo = "Contenido no legible"
            
            asunto = emoji.replace_emoji(asunto, replace='')
            cuerpo = emoji.replace_emoji(cuerpo, replace='')
            
            resumenes.append(
                {
                    "id": message["id"],
                    "remitente": remitente,
                    "asunto": asunto,
                    "cuerpo": cuerpo[:500]
                }
            )
            
            print(f"ID: {message["id"]}\nRemitente: {remitente}\nAsunto: {asunto}\nCuerpo: {cuerpo[:500]}\n\n")
            
    except HTTPError as error:
        print(f"An error occurred: {error}")
    
obtener_correos_hoy()