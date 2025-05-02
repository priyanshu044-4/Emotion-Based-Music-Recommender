document.getElementById('getRecommendations').addEventListener('click', () => {
    const emotion = document.getElementById('emotion').value;
    const errorDiv = document.getElementById('error');
    const recDiv = document.getElementById('recommendations');
    errorDiv.textContent = '';
    recDiv.innerHTML = '<p>Loading...</p>';

    fetch('http://localhost:5000/recommend-music', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ emotion: emotion })
    })
    .then(response => response.json())
    .then(data => {
        recDiv.innerHTML = '';

        if (data.error) {
            errorDiv.textContent = data.error;
            return;
        }

        if (!data.tracks || data.tracks.length === 0) {
            recDiv.innerHTML = '<p>No recommendations found.</p>';
            return;
        }

        data.tracks.forEach(track => {
            const trackDiv = document.createElement('div');
            trackDiv.className = 'track';

            const trackCard = document.createElement('div');
            trackCard.className = 'track-card';

            const trackCover = document.createElement('div');
            trackCover.className = 'track-cover';
            trackCover.style.backgroundImage = `url(${track.image})`;

            const trackInfo = document.createElement('div');
            trackInfo.className = 'track-info';

            const nameLink = document.createElement('a');
            nameLink.href = track.external_url;
            nameLink.target = '_blank';
            nameLink.rel = 'noopener noreferrer';
            nameLink.textContent = track.name;
            nameLink.className = 'track-name';

            const artistDiv = document.createElement('div');
            artistDiv.textContent = track.artist;
            artistDiv.className = 'track-artist';

            trackInfo.appendChild(nameLink);
            trackInfo.appendChild(artistDiv);

            trackCard.appendChild(trackCover);
            trackCard.appendChild(trackInfo);
            trackDiv.appendChild(trackCard);
            recDiv.appendChild(trackDiv);
        });
    })
    .catch(err => {
        recDiv.innerHTML = '';
        errorDiv.textContent = 'Error retrieving recommendations. Please try again later.';
        console.error(err);
    });
});
