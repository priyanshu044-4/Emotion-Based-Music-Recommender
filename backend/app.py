from flask import Flask, request, jsonify
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import os
from dotenv import load_dotenv
import logging
from flask_cors import CORS
import random

# Initialize Flask app
app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.DEBUG)

# Load environment variables
load_dotenv()

client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

if not client_id or not client_secret:
    raise ValueError("Spotify credentials not found in .env file.")

# Initialize Spotify
client_credentials_manager = SpotifyClientCredentials(
    client_id=client_id,
    client_secret=client_secret
)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Emotion to mood mapping
emotion_to_mood = {
    'Happy': 'upbeat',
    'Sad': 'calm',
    'Angry': 'intense',
    'Excited': 'energetic',
    'Relaxed': 'chill',
    'Bored': 'lofi',
    'Neutral': 'instrumental'
}

@app.route('/recommend-music', methods=['POST'])
def recommend_music():
    try:
        # Get emotion from the request body
        data = request.get_json()
        emotion = data.get('emotion')

        if not emotion:
            return jsonify({'error': 'Emotion is required'}), 400

        # Map emotion to mood for Spotify query
        mood = emotion_to_mood.get(emotion, 'instrumental')

        # Start by searching with an offset to avoid showing the same results
        offset = random.randint(0, 30)
        results = sp.search(q=mood, limit=20, offset=offset, type='track')

        # If no results found, return error
        if not results['tracks']['items']:
            return jsonify({'error': 'No tracks found for this mood'}), 404

        # Prepare the response with track details (no filtering by preview_url)
        tracks = []
        for track in results['tracks']['items'][:9]:  # Limit to 8 tracks
            tracks.append({
                'name': track['name'],
                'artist': track['artists'][0]['name'],
                'external_url': track['external_urls']['spotify'],
                'image': track['album']['images'][1]['url'] if len(track['album']['images']) > 1 else None,
            })

        return jsonify({'tracks': tracks})

    except Exception as e:
        app.logger.error(f"Error: {str(e)}")
        return jsonify({'error': f'Error retrieving recommendations: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
