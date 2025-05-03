import os
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy

load_dotenv()

client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

if not client_id or not client_secret:
    raise ValueError("Spotify credentials not set in environment variables.")

credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=credentials_manager)
