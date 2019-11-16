// include('/static/bitequick/slotmachine.min');

let pescatarian = false;
let lacto = false;
let vegan = false;
let gluten = false;

let currentGeoLocation = {
    latitude: 0,
    longitude: 0
};

document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('select');
    var instances = M.FormSelect.init(elems, {});
});

function showPosition(position) {
    const geoLocation = document.getElementById('geo_location');

    // round so that the gps point is not so ugly. We can assume an 11 meter bias, thats fine for this app
    const currentGeoLocation = {
        latitude: Math.round(position.coords.latitude * 10000) / 10000,
        longitude: Math.round(position.coords.longitude * 10000) / 10000
    };

    geoLocation.value = `[${currentGeoLocation.latitude}, ${currentGeoLocation.longitude}]`;
    geoLocation.focus();
}

function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition);
    }
}

function loadInputsWithParameters() {
    // get the current url
    const url = new URL(window.location.href);
    
    // pull geolocation from current url
    setTimeout(() => {
        const geoLocationElement = document.getElementById('geo_location');
        const geoLocationString = url.searchParams.get("geo_location");

        if (geoLocationString != null && geoLocationString.length > 0 && geoLocationElement != null) {
            const geoLocation = JSON.parse(geoLocationString);
            // store geolocation
            currentGeoLocation.latitude = geoLocation != null ? geoLocation[0] : currentGeoLocation.latitude;
            currentGeoLocation.longitude = geoLocation != null ? geoLocation[1] : currentGeoLocation.longitude;
            geoLocationElement.value = geoLocationString;
            geoLocationElement.style.textAlign = "right";
        }
    });
    // get range from current url
    setTimeout(() => {
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
    });

    // get the current dietary restrictions from the url
    const dietaryRestrictionStringArray = url.searchParams.getAll("dietary_restrictions");
    // loop through each restriction and select it in the mat select
    if (Array.isArray(dietaryRestrictionStringArray)) {
        dietaryRestrictionStringArray.forEach((currentDietaryRestriction) => {
            const dietaryTag = currentDietaryRestriction.split('-')[0].split(' ')[0];
            
            switch(dietaryTag) {
                case "pescatarian":
                    pescatarian = true;
                    break;
                case "lacto":
                    lacto = true;
                    break;
                case "vegan":
                    vegan = true;
                    break;
                case "gluten":
                    gluten = true;
                    break;
                default:
                    break;
            }
        });
    }
}

function setupSlotMachine() {
    const el = document.querySelector('#machine');
    const machine = new SlotMachine(el, {
        active: 1,
        delay: 450,
        auto: 1500
    });

    machine.shuffle();
}

loadInputsWithParameters();
setupSlotMachine();

if (currentGeoLocation == null || (currentGeoLocation.latitude === 0 && currentGeoLocation.longitude === 0)) {
    // get the location
    setTimeout(() => {
        getLocation();
    },100);
}