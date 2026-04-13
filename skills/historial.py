import json
import os
from datetime import datetime

ARCHIVO = "historial.json"

def cargar_historial():
    if os.path.exists(ARCHIVO):
        with open(ARCHIVO, "r") as f:
            return json.load(f)
    return []

def guardar_historial(new_data):
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_data = {
        "texto": new_data,
        "cuando": time
    }
    data = cargar_historial()
    data.append(new_data)
    with open(ARCHIVO, "w") as f:
        json.dump(data, f, indent=2)

def ver_historial():
    historial = cargar_historial()
    if len(historial) == 0:
        print("No existe historial")
    else:
        print("-----HISTORIAL-----")
        for data in historial:
            print(data)
        print("-------------------")
