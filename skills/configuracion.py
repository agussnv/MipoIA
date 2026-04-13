import json
import os

ARCHIVO = "config.json"

def cargar_config():
    if os.path.exists(ARCHIVO):
        with open(ARCHIVO, "r") as f:
            datos = json.load(f)
            return datos
    config = {
        "nombre": "Mipo",
        "bateria": 100
    }
    return config

def guardar_config(config):
    with open(ARCHIVO, "w") as f:
        json.dump(config, f, indent=2)

def cambiar_nombre(nuevo_nombre):
    datos = cargar_config()
    datos["nombre"] = nuevo_nombre
    guardar_config(datos)