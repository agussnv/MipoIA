import os
import sounddevice as sd # Captura el sonido del microfono y lo reproduce
import numpy as np # Librería matemática para arrays. Cada número es la amplitud de onda
import scipy.io.wavfile as wav # Guarda el array de números como un archivo .wav
import scipy.signal
import pygame # Para reproducir el sonido la voz. Forma más sencilla de hacerlo con PyGame.
import openwakeword # para activarse mediante la wake word
import time
import tempfile

os.environ["SDL_AUDIODRIVER"] = "alsa"
os.environ["AUDIODEV"] = "hw:2,0"

pygame.mixer.init() # Inicializa el sistema de audio para poder reproducir más adelante.

mipo_hablando = False

SAMPLE_RATE=44100 # mediciones por SEGUNDO que se hace del sonido
DEVICE=0
CHANNELS=1
SILENCIO_UMBRAL=100
SILENCIO_SEGUNDOS=2
TIMEOUT=10

_base = os.path.dirname(openwakeword.__file__)
WAKE_WORD_PATH = os.path.join(_base, "resources", "models", "alexa_v0.1.onnx")
WAKE_WORD_UMBRAL=0.5

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
        channels=CHANNELS,
        dtype=np.int16,
        device=DEVICE,
        blocksize=2756
    ) as stream:
        
        while True:
            chunk, _ = stream.read(2756)
            chunk = chunk.flatten()
            
            chunk_float = chunk.astype(np.float32)
            chunk_16k = scipy.signal.resample(chunk, 1280).astype(np.int16)
                
            prediccion = modelo_wakeword.predict(chunk_16k)
            score = list(prediccion.values())[0]
            print(f"SCORE: {score}")
        
            ahora = time.time()
            if score > WAKE_WORD_UMBRAL and (ahora - ultimo_activado) > COOLDOWN:
                ultimo_activado = ahora
                print("ACTIVADO")
                # return

def escuchar() -> str: # -> str es solamente de tipo informativo para quien lea el documento, no afecta funcionamiento.
    print("Escuchando...")
    
    grabando = False
    fragmentos = [] # donde almacenamos los chunks de audios (array de números que representan la amplitud de las ondas)
    chunk_size = int(SAMPLE_RATE*0.1) # Tamaño de muestras que leemos por 100ms (1600 muestras)
    segundos_silencio = 0
    segundos_timeout = 0
    
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype=np.int16) as stream: # abre el micrófono como un stream continuo. No se cierra hasta que no salgamos del bloque (with)
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
        
    archivo = tempfile.mktemp(suffix=".wav")
    wav.write(archivo, SAMPLE_RATE, audio)
    
    pygame.mixer.music.load(archivo)
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    os.remove(archivo)

esperar_wake_word()