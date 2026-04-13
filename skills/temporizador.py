import time
import threading
from skills.voz import hablar

def _contar(segundos):
    time.sleep(segundos)
    hablar(f"Temporizador de {segundos} segundos finalizado.")

def iniciar_temporizador(segundos):
    segundos = int(segundos)
    hilo = threading.Thread(target=_contar, args=(segundos,))
    hilo.daemon = True
    hablar(f"Temporizador de {segundos} segundos iniciado en segundo plano")
    hilo.start()