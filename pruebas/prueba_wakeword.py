import sounddevice as sd
import numpy as np
import openwakeword

DEVICE = 8
MODELO_PATH = "venv/lib/python3.13/site-packages/openwakeword/resources/models/alexa_v0.1.onnx"

modelo = openwakeword.Model(
    wakeword_model_paths=[MODELO_PATH]
)

print(f"Durmiendo... di 'Hey Jarvis' para activar")

with sd.InputStream(
    samplerate=16000,
    channels=1,
    dtype=np.int16,
    device=DEVICE,
    blocksize=1280
) as stream:
    while True:
        chunk, _ = stream.read(1280)
        chunk = chunk.flatten()
        
        volumen = np.abs(chunk).mean()
        # print(f"Volumen: {volumen:.0f}")
        
        prediccion = modelo.predict(chunk)
        score = list(prediccion.values())[0]
        # print(f"Score: {score}")
        
        if score > 0.5:
            print(f"Activado. Score: {score:.2f}")