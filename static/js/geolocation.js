// Get current position and set the latitude and longitude in the hidden input fields
function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(setPosition);
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}

function setPosition(position) {
    document.getElementById('latitude').value = position.coords.latitude;
    document.getElementById('longitude').value = position.coords.longitude;

    // For debugging purposes, you can also alert the coordinates or log them to the console
    console.log("Latitude: " + position.coords.latitude);
    console.log("Longitude: " + position.coords.longitude);
}

// Call the getLocation function as soon as the page loads
window.onload = getLocation;
