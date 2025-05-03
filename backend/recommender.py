import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv

load_dotenv()  # Make sure environment variables are loaded

def get_recommendations(emotion):
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET")
    ))

    emotion_to_genre = {
        "Happy": "party",
        "Sad": "acoustic",
        "Angry": "metal",
        "Excited": "edm",
        "Relaxed": "chill",
        "Bored": "ambient",
        "Neutral": "pop"
    }

    genre = emotion_to_genre.get(emotion, "pop")

    results = sp.recommendations(seed_genres=[genre], limit=5)
    tracks = []
    for track in results['tracks']:
        tracks.append({
            "name": track['name'],
            "artist": track['artists'][0]['name'],
            "external_url": track['external_urls']['spotify']
        })
    return tracks
