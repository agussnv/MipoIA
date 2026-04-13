import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import whisper

DURACION = 5
SAMPLE_RATE = 16000
DEVICE = 8

modelo = whisper.load_model("small")
print(f"Modelo cargado. Grabando {DURACION} segundos... Habla ahora.")

audio = sd.rec(
    int(DURACION * SAMPLE_RATE),
    samplerate=SAMPLE_RATE,
    channels=1,
    dtype=np.int16,
    device=DEVICE
)

sd.wait()
print("Grabación terminada. Transcribiendo...")

wav.write("temp.wav", SAMPLE_RATE, audio)

transcription = modelo.transcribe("temp.wav", language="es")
print(f"Transcripción: {transcription['text']}")