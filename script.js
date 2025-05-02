document.getElementById('getRecommendations').addEventListener('click', () => {
    const emotion = document.getElementById('emotion').value;
    const errorDiv = document.getElementById('error');
    const recDiv = document.getElementById('recommendations');
    const button = document.getElementById('getRecommendations');

    errorDiv.textContent = ''; // Clear previous errors
    recDiv.innerHTML = '<div class="spinner"></div>'; // Show loading spinner
    button.disabled = true; // Disable button to prevent multiple clicks

    // Add a cache buster to avoid fetching the same results (Spotify might cache similar queries)
    const url = `http://localhost:5000/recommend-music?ts=${Date.now()}`;

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ emotion: emotion })
    })
    .then(response => response.json())
    .then(data => {
        recDiv.innerHTML = ''; // Clear loading message
        button.disabled = false; // Re-enable button

        if (data.error) {
            errorDiv.textContent = data.error;
            return;
        }

        if (!data.tracks || data.tracks.length === 0) {
            recDiv.innerHTML = '<p>No recommendations found.</p>';
            return;
        }

        // Create carousel container
        const carouselContainer = document.createElement('div');
        carouselContainer.className = 'carousel-container';

        // Recommendations list (horizontal scroll)
        const recommendationsList = document.createElement('div');
        recommendationsList.className = 'recommendations';

        // Append tracks to recommendations
        data.tracks.forEach(track => {
            const trackDiv = document.createElement('div');
            trackDiv.className = 'track';

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

            trackDiv.appendChild(trackCover);
            trackDiv.appendChild(trackInfo);

            recommendationsList.appendChild(trackDiv);
        });

        // Append the recommendations to the carousel
        carouselContainer.appendChild(recommendationsList);

        // Append the carousel container to the recommendations div
        recDiv.appendChild(carouselContainer);

        // Adding a fade-in effect for recommendations
        setTimeout(() => {
            carouselContainer.classList.add('show');
        }, 100);  // Delay the fade-in for a smoother effect

    })
    .catch(err => {
        recDiv.innerHTML = '';
        errorDiv.textContent = 'Error retrieving recommendations. Please try again later.';
        console.error(err);
        button.disabled = false; // Re-enable button even if an error occurs
    });
});
