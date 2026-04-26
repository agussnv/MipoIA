import os
from dotenv import load_dotenv
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

CLIENT_ID=os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET=os.getenv("SPOTIFY_CLIENT_SECRET")
ARCHIVO="spotify_devices.json"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri="http://127.0.0.1:3000",
    scope="user-read-playback-state user-modify-playback-state user-read-currently-playing streaming user-library-modify"
))

# result = sp.search(q=f"artist:Shakira", type="track", limit=10)

# for track in result['tracks']['items']:
#     print(f"Nombre: {track['name']}")


# print(result['tracks']['items'][1]['name'])

# Obtener dispositivos con Spotify abierto
def devices():
    result = sp.devices()
    return result

# Obtener información de la reproducción actual (device, track, artist...)
def current_playback():
    result = sp.current_playback()
    return result

def current_playback_formatted():
    result = current_playback()
    device = result['device']
    return (f"Escuchando ahora '{result['item']['name']}' desde {device['name']} ({device['type']})")
    
def get_info_device():
    current = current_playback()
    device = current['device']
    return device

# Comenzar reproducción
def start_playback():
    current = current_playback()
    if not current['is_playing']:
        sp.start_playback()

# Pausar reproducción
def pause_playback():
    current = current_playback()
    if current['is_playing']:    
        sp.pause_playback()

# Pasar a la siguiente canción
def next_track():
    sp.next_track()

# Pasar a la anterior canción
def previous_track():
    sp.previous_track()

# Setear volumen (en smartphone no funciona)
def set_volume(volume_percent):
    device = get_info_device()
    if device['type'] == 'Computer':
        sp.volume(volume_percent)

# Pasar de un dispositivo a otro la reproducción. Lo ideal es utilizar esto luego de haber
# utilizado devices() y preguntarle al usuario a cual de los activos desea pasar la canción.
def transfer_playback(device_name):
    # Considero que no es la mejor alternativa, ya que debe coincidir el nombre exacto, y
    # al estar por voz, puede tener fallos y nunca encontrarlo. Buscaría la forma de hacerlo
    # que Mipo lo buscase directamente desde el JSON que devuelve devices()
    if os.path.exists(ARCHIVO):
        with open(ARCHIVO, "r") as f:
            devices = json.load(f)
            result = next((item for item in devices if item['name'] == device_name), None)
    if result:
        sp.transfer_playback(result['id'])
    
devices()