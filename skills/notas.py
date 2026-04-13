import json
import os

ARCHIVO = "notas.json"

def cargar_notas():
    if os.path.exists(ARCHIVO):
        with open(ARCHIVO, "r") as f:
            return json.load(f)
    return []

def guardar_notas(notas):
    with open(ARCHIVO, "w") as f:
        json.dump(notas, f, indent=2)
    
def añadir_nota(nota):
    notas = cargar_notas()
    notas.append(nota)
    guardar_notas(notas)

def ver_notas():
    notas = cargar_notas()
    if len(notas) == 0:
        print("No hay notas guardadas")
    else:
        print("---- Tus notas ----")
        for i, nota in enumerate(notas):
            print(f"{i+1}. {nota}")
        print("-------------------")