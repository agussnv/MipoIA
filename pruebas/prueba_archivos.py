with open("notas.txt", "a") as archivo:
    archivo.write("Primera nota del robot\n")
    archivo.write("Segunda nota\n")

with open("notas.txt", "r") as archivo:
    contenido = archivo.read()
    print(contenido)

with open("notas.txt", "a") as archivo:
    archivo.write("Esto es con un append\n")

with open("notas.txt", "r") as archivo:
    contenido = archivo.read()
    print(contenido)