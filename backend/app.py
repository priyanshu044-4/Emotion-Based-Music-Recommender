from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import random
from spotify_client import sp  # imported shared Spotify client

# Initialize Flask app
app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.DEBUG)

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
        data = request.get_json()
        emotion = data.get('emotion')

        if not emotion:
            return jsonify({'error': 'Emotion is required'}), 400

        mood = emotion_to_mood.get(emotion, 'instrumental')
        offset = random.randint(0, 30)
        results = sp.search(q=mood, limit=20, offset=offset, type='track')

        if not results['tracks']['items']:
            return jsonify({'error': 'No tracks found for this mood'}), 404

        tracks = []
        for track in results['tracks']['items'][:9]:
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
