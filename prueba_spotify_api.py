import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()

CLIENT_ID=os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET=os.getenv("SPOTIFY_CLIENT_SECRET")

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(CLIENT_ID, CLIENT_SECRET))

result = sp.search(q="Shakira", type="artist", limit=1)

print(result)