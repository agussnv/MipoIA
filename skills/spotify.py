import os
from dotenv import load_dotenv
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from rapidfuzz import process

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
    result = sp.devices()['devices']
    print(result)
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

# Comenzar reproducción (QUE PREGUNTE DONDE QUIERE QUE REPRODUZCAS LA MÚSICA EN CASO DE NO HABER NINGÚN DISPOSITIVO ACTIVO)
def start_playback(name=None):
    lista_devices = devices()
    device_active = next((d for d in lista_devices if d['is_active'] == True), None)
    if not device_active and not name:
        return {
            "pendiente": True,
            "pregunta": "No hay ningún dispositivo activo. ¿En qué dispositivo quieres reproducir?",
            "skill": "start_spotify"
        }

    if not device_active:
        transfer_playback(name)
        return

    current = current_playback()
    if not current or not current['is_playing']:
        sp.start_playback(device_active['id'])
    # hablar("No hay dispositivos activos")

# Pausar reproducción
def pause_playback():
    current = current_playback()
    if current['is_playing']:    
        sp.pause_playback()
        # hablar("Música pausada")

# Pasar a la siguiente canción
def next_track():
    sp.next_track()
    # hablar("Hecho")

# Pasar a la anterior canción
def previous_track():
    sp.previous_track()
    # hablar("Hecho")

# Setear volumen (en smartphone no funciona)
def set_volume(volume_percent):
    device = get_info_device()
    if device['type'] == 'Computer' or device['type'] == "TV":
        sp.volume(volume_percent)

def search_device_alias(name):
    if os.path.exists(ARCHIVO):
        with open(ARCHIVO, "r") as f:
            devices = json.load(f)
            for d in devices:
                for alias in d['alias']:
                    if alias.lower() == name.lower():
                        print(d)
                        return d['name']
    return None

def search_device_fuzzy(name, devices_spotify):
    result = process.extractOne(name, devices_spotify)
    print(result)
    if result and result[1] > 55:
        return result[0]
    return None

def find_device(name):
    device_name = search_device_alias(name)
    if device_name:
        return device_name
    
    devices_spotify = devices()
    names = [d['name'] for d in devices_spotify]
    device_name = search_device_fuzzy(name, names)
    if device_name:
        return device_name
    
    return None
    
def transfer_playback(name):
    name = find_device(name)
    if not name:
        # hablar(f"El dispositivo {name} no existe")
        return
    devices_spotify = devices()
    device = next((d for d in devices_spotify if d['name'] == name), None)
    if device:
        sp.transfer_playback(device['id'], force_play=True)
    # else:
        # hablar(f"El dispositivo {name} no está activo en este momento")

def save_song():
    track = current_playback()
    is_already = sp.current_user_saved_tracks_contains(f"spotify:track:{track['item']['id']}")
    if not is_already:
        sp.current_user_saved_tracks_add([track['item']['id']])
        print("Canción guardada")
        
devices()