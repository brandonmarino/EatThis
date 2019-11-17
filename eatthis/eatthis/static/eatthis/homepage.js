/**
 * Display the current location to the geo location element
 * @param {*} position the position from getCurrentPosition
 */
function showPosition(position) {
    const geoLocation = document.getElementById('geo_location');

    // round so that the gps point is not so ugly. We can assume an 11 meter bias, thats fine for this app
    const currentGeoLocation = {
        latitude: Math.round(position.coords.latitude * 10000) / 10000,
        longitude: Math.round(position.coords.longitude * 10000) / 10000
    };

    // get the location value
    geoLocation.value = `[${currentGeoLocation.latitude}, ${currentGeoLocation.longitude}]`;
    geoLocation.focus();
}

/**
 * Enable the submit button for the form
 */
function enableSubmitButton() {
    // enable the eat button
    const submitButtonElement = document.getElementById('submit-button');
    submitButtonElement.disabled = false;
}

/**
 * Setup the location search and handlers for when the location is found
 */
function setupLocationSearch() {
    if (navigator.geolocation) {
        var options = {
            enableHighAccuracy: true,
            timeout: 5000,
            maximumAge: 0
        };

        // get the location, display it and enable the submit button
        navigator.geolocation.getCurrentPosition((coords) => {
            showPosition(coords);
            enableSubmitButton();
        }, (error) => {
            console.error(error);
        }, options);
    }
}

/**
 * Take inputs from the url and preload the inputs with those values
 */
function loadInputsWithParameters() {
    // get the current url
    const url = new URL(window.location.href);
    const attemptsElement = document.getElementById('attempts');
    const attemptsString = url.searchParams.get("attempts");

    if (attemptsString != null && attemptsString.length > 0 && attemptsElement != null) {
        const attempts = +attemptsString + 1;
        attemptsElement.value = ''+attempts;
    } else {
        attemptsElement.value = ''+1;
    }

    // get range from current url
    const rangeElement = document.getElementById('range');
    const rangeString = url.searchParams.get("range");
    if (rangeString != null && rangeElement != null) {
        const range = JSON.parse(rangeString);
        rangeElement.value = range;
        rangeElement.style.textAlign = "right";
    }

    const dietaryElement = document.getElementById('dietary_restrictions');
    if (dietaryElement != null) {
        dietaryElement.style.textAlign = "right";
    }
}

/**
 * Initialize the select component
 */
function setupSelectElement() {
    document.addEventListener('DOMContentLoaded', function() {
        var elems = document.querySelectorAll('select');
        M.FormSelect.init(elems, {});
    });    
}

// set up the select
setupSelectElement();
// get the location and enable the submit button after
setupLocationSearch();
// load inputs with url params
loadInputsWithParameters();
