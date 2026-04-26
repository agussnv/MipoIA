import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

CLIENT_ID=os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET=os.getenv("SPOTIFY_CLIENT_SECRET")

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
result = sp.devices()

for device in result['devices']:
    print(f"Device name: {device['name']} ({device['type']})\nDevice id: {device['id']}\n")

device_id_1=result['devices'][0]['id']

if len(result['devices']) > 1:
    device_id_2=result['devices'][1]['id']



# Obtener información (nombre) de la canción que está sonando
result = sp.current_playback()
device = result['device']
print(f"Escuchando ahora '{result['item']['name']}' desde {device['name']} ({device['type']})")



# Comenzar reproducción
if not result['is_playing']:
    sp.start_playback()



# Pausar reproducción
# if result['is_playing']:
#     sp.pause_playback()
    


# Pasar a la siguiente canción
# sp.next_track()

# Pasar a la anterior canción
# sp.previous_track()



# Setear volumen (en smartphone no funciona)
if device['type'] == 'Computer':
    sp.volume(volume_percent=100)



# Pasar de un dispositivo a otro la reproducción
if device['id'] == device_id_1:
    sp.transfer_playback(device_id_2)
else:
    sp.transfer_playback(device_id_1)