import json

config = {
    "nombre": "Mipo",
    "bateria": 95.5,
    "historial": ["hola", "baja el volumen", "salir"]
}

with open("config.json", "w") as archivo:
    json.dump(config, archivo, indent=2)

print("Guardado")

with open("config.json", "r") as archivo:
    datos = json.load(archivo)

print(datos["nombre"])
print(datos["bateria"])