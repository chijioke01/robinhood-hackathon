// Get the data from the server

let data = [
    {
      name: "Grafitti",
      status: "resolved",
      lat: 42.7098112,
      long: -73.2069888,
    },
    {
      name: "Abandoned Vehicles",
      status: "submitted",
      lat: 42.712082,
      long: -73.218619,
    },
  ];
  
  // filter the data using name
  const issueName = document.querySelector(".map__select");
  issueName.addEventListener("change", (event) => {
    if (event.target.value) {
      data = data.filter((issue) =>
        issue.name.toLowerCase().includes(event.target.value)
      );
    }
  
    // Remove all the markers
    removeAllMarkers();
  
    // add only the markers passing the condition
    data.forEach((item) => {
      let marker = L.marker([item.lat, item.long]).addTo(map);
      marker.bindPopup(`<b>${item.name}</b> <br> ${item.status}`);
    });
  });
  
  // Function to remove all markers from the map
  function removeAllMarkers() {
    map.eachLayer(function (layer) {
      if (layer instanceof L.Marker) {
        map.removeLayer(layer);
      }
    });
  }
  
  // check if the user needs a custom centered map
  const detectLocation = document.querySelector(".detect__location");
  detectLocation.addEventListener("click", (event) => {
    userCenteredMap();
  });
  
  const map = L.map("map").setView([37.0902, -95.7129], 5);
  usCenteredMap();
  
  function usCenteredMap() {
    // recenter the map
    map.setView([37.0902, -95.7129], 5);
  
    L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 19,
      attribution:
        '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    }).addTo(map);
  
    // Add the issues to the map
    data.forEach((item) => {
      let marker = L.marker([item.lat, item.long]).addTo(map);
      marker.bindPopup(`<b>${item.name}</b> <br> ${item.status}`);
    });
  }
  
  function userCenteredMap() {
    // Get the user location using the geolocation API
    navigator.geolocation.getCurrentPosition(
      (position) => {
        const lat = position.coords.latitude;
        const long = position.coords.longitude;
  
        // Recenter the map
        map.setView([lat, long], 13);
      },
  
      (error) => {
        alert(
          "Failed to get your coordinates, check your browser geolocation permissions and try again"
        );
        usCenteredMap();
      }
    );
  }