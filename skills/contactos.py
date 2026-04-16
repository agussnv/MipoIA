import json
import os
import unicodedata

ARCHIVO = "contactos.json"

def normalizar(nombre):
    nombre = nombre.lower()
    nombre = unicodedata.normalize('NFD', nombre)
    nombre = ''.join(c for c in nombre if unicodedata.category(c) != 'Mn')
    return nombre


def buscar_contacto(nombre):
    if os.path.exists(ARCHIVO):
        with open(ARCHIVO, "r") as f:
            contactos = json.load(f)
            resultado = next((item for item in contactos if item['name'] == normalizar(nombre)), None)
            return resultado
    return {}
