import sounddevice as sd # Captura el sonido del microfono y lo reproduce
import numpy as np # Librería matemática para arrays. Cada número es la amplitud de onda
import scipy.io.wavfile as wav # Guarda el array de números como un archivo .wav
import whisper # Modelo de transcripción de voz a texto
import edge_tts # De texto a voz. Envía el texto a sus servidores y devuelve .mp3
import pygame # Para reproducir el sonido la voz. Forma más sencilla de hacerlo con PyGame.
import asyncio # edge_tts es una librería asíncrona. Para que sea asíncrona su espera.
import openwakeword # para activarse mediante la wake word
import time
import os
import tempfile

SAMPLE_RATE=16000 # mediciones por SEGUNDO que se hace del sonido
DEVICE=8
SILENCIO_UMBRAL=1000
SILENCIO_SEGUNDOS=2
_base = os.path.dirname(openwakeword.__file__)
WAKE_WORD_PATH = os.path.join(_base, "resources", "models", "alexa_v0.1.onnx")
WAKE_WORD_UMBRAL=0.5
TIMEOUT=10

mipo_hablando = False

modelo_whisper = whisper.load_model("small") # Carga el modelo que utilizará: base -> small -> medium...
pygame.mixer.init() # Inicializa el sistema de audio para poder reproducir más adelante.

def hay_voz(audio_chunk): # audio_chunk son 100ms de audio, un conjunto de números que representa la onda de sonido
    return np.abs(audio_chunk).mean() > SILENCIO_UMBRAL
    # np.abs(array_numerico) transforma todos los números a positivos. Ya que nos interesa su amplitud, no su signo
    # .mean() calcula la media entre todos estos números. Si están por debajo de SILENCIO_UMBRAL, es que no hay sonido
    # por eso luego se le suma 0.1 (100ms) a la cantidad de audio sin voz y va almacenando esas ondas en fragmentos.

def esperar_wake_word():
    global modelo_wakeword
    modelo_wakeword = openwakeword.Model(wakeword_model_paths=[WAKE_WORD_PATH])
    
    print("Durmiendo... Di 'Alexa' para activar")
    
    ultimo_activado=0
    COOLDOWN=5
    
    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype=np.int16,
        device=DEVICE,
        blocksize=1280
    ) as stream:
        
        while True:
            chunk, _ = stream.read(1280)
            chunk = chunk.flatten()
                
            prediccion = modelo_wakeword.predict(chunk)
            score = list(prediccion.values())[0]
        
            ahora = time.time()
            if score > WAKE_WORD_UMBRAL and (ahora - ultimo_activado) > COOLDOWN:
                ultimo_activado = ahora
                print("ACTIVADO")
                return 

def escuchar() -> str: # -> str es solamente de tipo informativo para quien lea el documento, no afecta funcionamiento.
    print("Escuchando...")
    
    grabando = False
    fragmentos = [] # donde almacenamos los chunks de audios (array de números que representan la amplitud de las ondas)
    segundos_silencio = 0
    segundos_timeout = 0
    chunk_size = int(SAMPLE_RATE*0.1) # Tamaño de muestras que leemos por 100ms (1600 muestras)
    
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype=np.int16, device=DEVICE) as stream: # abre el micrófono como un stream continuo. No se cierra hasta que no salgamos del bloque (with)
        while True:
            chunk, _ = stream.read(chunk_size) # devuelve 2 cosas, el audio (100ms) y estado overflow (si el buffer se llenó). chunk, _ significa: guardame el primer valor en chunk, el segundo no me interesa
            
            if hay_voz(chunk):
                if not grabando:
                    print("Grabando...")
                    grabando = True
                fragmentos.append(chunk)
                segundos_silencio = 0
            elif grabando:
                fragmentos.append(chunk)
                segundos_silencio += 0.1
                
                if segundos_silencio >= SILENCIO_SEGUNDOS:
                    print("Procesando...")
                    break
            else:
                if not mipo_hablando:
                    segundos_timeout += 0.1
                if segundos_timeout >= TIMEOUT:
                    return ""

    audio = np.concatenate(fragmentos) # Une todos los chunks grabados.
    
    archivo = tempfile.mktemp(suffix=".wav") # Crea el archivo temporal
    wav.write(archivo, SAMPLE_RATE, audio) # Guarda el audio dentro del archivo, siguiendo la estructura del ratio definido
    resultado = modelo_whisper.transcribe(archivo, language="es", fp16=False) # Transcribe el archivo a texto
    os.remove(archivo) # Borra el archivo temporal
    
    transcripcion = resultado["text"].strip() # Elimina de la transcripción los espacios en blanco y saltos de linea en el inicio y final.
    print(f"Tú: {transcripcion}")
    return transcripcion

def hablar(texto: str):
    global mipo_hablando
    mipo_hablando = True

    print(f"Mipo: {texto}")
    
    async def _generar():
        comunicacion = edge_tts.Communicate(texto, voice="es-ES-AlvaroNeural")
        archivo = tempfile.mktemp(suffix=".mp3")
        await comunicacion.save(archivo)
        return archivo
    
    archivo = asyncio.run(_generar()) # Ejecuta la función asíncrona. Crea un bucle de eventos, ejecuta _generar hasta que termina y devuelve el resultado
    
    pygame.mixer.music.load(archivo)
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10) # Entra en bucle hasta terminar de estar ocupado. Lo verifica cada 100ms.
    
    os.remove(archivo)
    mipo_hablando = False