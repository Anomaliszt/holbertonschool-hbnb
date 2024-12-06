const API_BASE_URL = 'http://localhost:5000/api/v1';
const ENDPOINTS = {
    LOGIN: '/auth/login',
    PLACES: '/places',
    REVIEWS: '/reviews'
};

// COOKIES UTILITIES
const cookieUtils = {
    setCookie(name, value, days = 7) {
        const expires = new Date(Date.now() + days * 864e5).toUTCString();
        document.cookie = `${name}=${encodeURIComponent(value)}; expires=${expires}; path=/; Secure; SameSite=Strict`;
    },
    getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        return parts.length === 2 ? decodeURIComponent(parts.pop().split(';').shift()) : null;
    },
    deleteCookie(name) {
        document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/`;
    }
};

// AUTH UTILITIES
const authUtils = {
    isLoggedIn: () => !!cookieUtils.getCookie('token'),
    getToken: () => cookieUtils.getCookie('token'),
    setToken: (token) => cookieUtils.setCookie('token', token),
    removeToken: () => cookieUtils.deleteCookie('token'),
    logout: () => {
        authUtils.removeToken();
        window.location.href = 'login.html';
    }
};

// API UTILITIES
const apiUtils = {
    async fetchWithAuth(url, options = {}) {
        const headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            ...(authUtils.isLoggedIn() && { 'Authorization': `Bearer ${authUtils.getToken()}` })
        };

        try {
            const response = await fetch(url, { ...options, headers, mode: 'cors' });
            if (response.status === 401) authUtils.logout();
            return response;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    },
    getQueryParam: (param) => new URLSearchParams(window.location.search).get(param)
};

// UI UTILITIES
const uiUtils = {
    updateLoginButton() {
        const loginLink = document.getElementById('login-link');
        if (!loginLink) return;

        const isLoggedIn = authUtils.isLoggedIn();
        loginLink.textContent = isLoggedIn ? 'Logout' : 'Login';
        loginLink.href = isLoggedIn ? '#' : 'login.html';

        if (isLoggedIn) {
            loginLink.onclick = (e) => {
                e.preventDefault();
                authUtils.logout();
            };
        }
    },
    displayErrorMessage(elementId, message) {
        const element = document.getElementById(elementId);
        if (element) {
            element.textContent = message;
            element.style.display = 'block';
        }
    },
    renderOptions(selectElement, options, defaultLabel = 'Select') {
        if (!selectElement) return;
        selectElement.innerHTML = options
            .map((opt) => `<option value="${opt.value}">${opt.label}</option>`)
            .join('');
        selectElement.insertAdjacentHTML('afterbegin', `<option value="">${defaultLabel}</option>`);
    }
};

// PLACE HANDLERS
let originalPlaces = [];

const placeHandlers = {
    async fetchPlaces() {
        try {
            const response = await apiUtils.fetchWithAuth(`${API_BASE_URL}${ENDPOINTS.PLACES}`);
            if (!response.ok) throw new Error('Failed to fetch places');

            originalPlaces = await response.json();
            placeHandlers.displayPlaces(originalPlaces);
        } catch (error) {
            console.error('Fetch places error:', error);
            uiUtils.displayErrorMessage('places-list', 'Failed to load places. Please try again later.');
        }
    },
    displayPlaces(places) {
        const placesList = document.getElementById('places-list');
        if (!placesList) return;

        placesList.innerHTML = places.length
            ? places.map(placeHandlers.createPlaceHTML).join('')
            : '<div class="no-places"><p>No places available</p></div>';
    },
    createPlaceHTML(place) {
        return `
            <article class="place">
                <div class="place-header">
                    <h2>${place.title || 'Unnamed Place'}</h2>
                </div>
                <div class="place-details">
                    <p><strong>Price per night:</strong> $${place.price}</p>
                </div>
                <div class="place-footer">
                    <a href="place.html?id=${place.id}" class="view-details">View Details</a>
                </div>
            </article>`;
    },
    filterPlaces(price) {
        const filteredPlaces = price === 'All'
            ? originalPlaces
            : originalPlaces.filter((place) => place.price && parseFloat(place.price) <= parseInt(price));
        placeHandlers.displayPlaces(filteredPlaces);
    }
};

// REVIEW FORM HANDLING
function initializeReviewForm() {
    const reviewForm = document.getElementById('add-review-form');
    if (!reviewForm) return;

    if (!authUtils.isLoggedIn()) {
        window.location.href = 'index.html';
        return;
    }

    reviewForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const placeId = apiUtils.getQueryParam('id');
        if (!placeId) {
            alert('Place ID is missing.');
            return;
        }

        const reviewText = document.getElementById('review-text').value;
        const reviewRating = document.getElementById('review-rating').value;

        try {
            const response = await apiUtils.fetchWithAuth(
                `${API_BASE_URL}${ENDPOINTS.PLACES}/${placeId}/reviews`,
                {
                    method: 'POST',
                    body: JSON.stringify({
                        text: reviewText,
                        rating: parseInt(reviewRating, 10),
                    }),
                }
            );

            if (response.ok) {
                const successMessage = document.getElementById('success-message');
                if (successMessage) {
                    successMessage.textContent = 'Review submitted successfully!';
                    successMessage.style.display = 'block';
                }

                reviewForm.reset();
            } else {
                const errorData = await response.json();
                uiUtils.displayErrorMessage('error-message', errorData.error || 'Failed to submit review.');
            }
        } catch (error) {
            console.error('Error submitting review:', error);
            uiUtils.displayErrorMessage('error-message', 'Network error occurred. Please try again.');
        }
    });
}

// Initialize the login form
function initializeLoginForm() {
    const loginForm = document.getElementById('login-form');
    if (!loginForm) return;

    loginForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        try {
            const response = await fetch(`${API_BASE_URL}${ENDPOINTS.LOGIN}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({ email, password })
            });

            const data = await response.json();

            if (response.ok && data.access_token) {
                authUtils.setToken(data.access_token);
                window.location.href = 'index.html';
            } else {
                uiUtils.displayErrorMessage('error-message', data.error || 'Invalid credentials');
            }
        } catch (error) {
            uiUtils.displayErrorMessage('error-message', 'Network error occurred. Please try again.');
        }
    });
}

// INIT LIST OF PLACES
function initializePlacesList() {
    const placesListElement = document.getElementById('places-list');
    if (!placesListElement) return;

    placeHandlers.fetchPlaces();
}

// INIT PRICE FILTER
function initializePriceFilter() {
    const priceFilter = document.getElementById('price-filter');
    if (!priceFilter) return;

    uiUtils.renderOptions(priceFilter, [
        { value: '10', label: '$10 or less' },
        { value: '50', label: '$50 or less' },
        { value: '100', label: '$100 or less' },
        { value: 'All', label: 'All Prices' }
    ]);

    priceFilter.addEventListener('change', (e) => {
        placeHandlers.filterPlaces(e.target.value);
    });
}

// PLACE DETAILS HANDLER
async function initializePlaceDetails() {
    const placeDetailsContainer = document.getElementById('place-details');
    if (!placeDetailsContainer) return;

    const placeId = apiUtils.getQueryParam('id');
    if (!placeId) {
        window.location.href = 'index.html';
        return;
    }

    try {
        const [placeResponse, reviewsListResponse] = await Promise.all([
            apiUtils.fetchWithAuth(`${API_BASE_URL}${ENDPOINTS.PLACES}/${placeId}`),
            apiUtils.fetchWithAuth(`${API_BASE_URL}${ENDPOINTS.REVIEWS}/places/${placeId}/reviews`)
        ]);

        if (!placeResponse.ok) throw new Error('Failed to fetch place details');
        const place = await placeResponse.json();
        
        const hostResponse = await apiUtils.fetchWithAuth(`${API_BASE_URL}/users/${place.owner}`);
        if (!hostResponse.ok) throw new Error('Failed to fetch host details');
        const host = await hostResponse.json();

        const reviewsList = reviewsListResponse.ok ? await reviewsListResponse.json() : [];

        // Fetch Details, to get REVIEW INFO, then REVIEWER INFO
        const reviewsWithDetails = await Promise.all(
            reviewsList.map(async (review) => {
                // REVIEW INFO
                const reviewResponse = await apiUtils.fetchWithAuth(`${API_BASE_URL}${ENDPOINTS.REVIEWS}/${review.id}`);
                const reviewDetails = await reviewResponse.json();

                // REVIEWER INFO
                const userResponse = await apiUtils.fetchWithAuth(`${API_BASE_URL}/users/${reviewDetails.user_id}`);
                const userDetails = await userResponse.json();

                return {
                    ...reviewDetails,
                    reviewer: `${userDetails.first_name} ${userDetails.last_name}`
                };
            })
        );

        const amenitiesList = place.amenities && place.amenities.length 
            ? place.amenities.map(amenity => amenity.name).join(', ')
            : 'No amenities available';

        const reviewsHTML = reviewsWithDetails.length 
            ? reviewsWithDetails.map(review => `
                <div class="review">
                    <div class="reviewer-info">
                        <strong>Reviewed by ${review.reviewer}</strong>
                    </div>
                    <p class="review-text">${review.text}</p>
                    <div class="rating">Rating: ${'★'.repeat(review.rating)}${'☆'.repeat(5-review.rating)}</div>
                </div>
            `).join('')
            : '<p>No reviews yet</p>';

        placeDetailsContainer.innerHTML = `
            <article class="place-full">
                <h1>${place.title}</h1>
                <div class="place-info">
                    <p><strong>Host:</strong> ${host.first_name} ${host.last_name}</p>
                    <p><strong>Price per night:</strong> $${place.price}</p>
                    <p><strong>Description:</strong> ${place.description || 'No description available'}</p>
                    <p><strong>Amenities:</strong> ${amenitiesList}</p>
                </div>
                <div class="reviews-section">
                    <h2>Reviews</h2>
                    <div class="reviews-list">
                        ${reviewsHTML}
                    </div>
                </div>
            </article>`;
    } catch (error) {
        console.error('Error fetching details:', error);
        placeDetailsContainer.innerHTML = '<p class="error">Failed to load place details</p>';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    uiUtils.updateLoginButton();
    initializeLoginForm();
    initializePlacesList();
    initializePriceFilter();
    initializeReviewForm();
    initializePlaceDetails();
});
