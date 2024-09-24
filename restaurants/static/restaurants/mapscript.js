let map;
let service;
let favorites = []; // Array to store favorite restaurants

function initMap() {
    const atlanta = { lat: 33.749, lng: -84.388 };

    // Initialize the map centered on Atlanta
    map = new google.maps.Map(document.getElementById('map'), {
        center: atlanta,
        zoom: 12
    });

    // Request object for the Google Places API
    const request = {
        location: atlanta,
        radius: '5000', // 5 km radius
        type: ['restaurant'] // Search for restaurants
    };

    // Initialize the Places service
    service = new google.maps.places.PlacesService(map);

    // Perform nearby search to get restaurants
    service.nearbySearch(request, handleSearchResults);
}

function getCuisineType(place) {
const cuisineMap = {
'chinese': 'Chinese',
'italian': 'Italian',
'japanese': 'Japanese',
'mexican': 'Mexican',
'thai': 'Thai',
'indian': 'Indian',
'korean': 'Korean',
'vietnamese': 'Vietnamese',
'greek': 'Greek',
'french': 'French',
'spanish': 'Spanish',
'american': 'American',
// Add more mappings as needed
};

// Extract types that indicate cuisine
const cuisines = place.types
.map(type => cuisineMap[type.toLowerCase()] || null)
.filter(cuisine => cuisine !== null);

// If no specific cuisine types are found, return 'Cuisine: Not Specified'
return cuisines.length > 0 ? cuisines.join(', ') : 'Cuisine: Not Specified';
}


function handleSearchResults(results, status) {
    if (status === google.maps.places.PlacesServiceStatus.OK) {
        const restaurantList = document.getElementById('restaurant-list');
        restaurantList.innerHTML = ''; // Clear previous results

        // Loop through each result (restaurant)
        results.forEach((place) => {
            // Add marker for each restaurant on the map
            const marker = new google.maps.Marker({
                map: map,
                position: place.geometry.location,
                title: place.name
            });

            // Create the restaurant item HTML
            const restaurantItem = document.createElement('div');
            restaurantItem.className = 'restaurant-item';
            restaurantItem.innerHTML = `
                <div class="icon favorite" data-id="${place.place_id}">☆</div>
                <div class="restaurant-info">
                    <p>Cuisine: ${getCuisineType(place)}</p>
                    <h3>${place.name}</h3>
                    <a href="#">See Details</a>
                </div>
            `;


            // Add event listener to center the map on restaurant when clicked
            restaurantItem.addEventListener('click', () => {
                map.panTo(place.geometry.location);
                map.setZoom(17);
            });

            // Add event listener to toggle favorite status
            restaurantItem.querySelector('.favorite').addEventListener('click', function(event) {
                event.stopPropagation(); // Prevent triggering the restaurant click event
                const placeId = this.getAttribute('data-id');

                // Toggle favorite status
                if (favorites.includes(placeId)) {
                    favorites = favorites.filter(id => id !== placeId);
                    this.textContent = '☆'; // Change to hollow star
                } else {
                    favorites.push(placeId);
                    this.textContent = '★'; // Change to filled star
                }

                console.log('Favorites:', favorites); // Debug: log favorites
            });

            // Append the restaurant item to the list
            restaurantList.appendChild(restaurantItem);
        });
    }
}