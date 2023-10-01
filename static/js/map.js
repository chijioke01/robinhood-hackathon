// Get the data from the server

const unfilteredData = generateDummyData();
let data = [...unfilteredData];

// filter the data using name
const issueName = document.querySelector(".map__select");
issueName.addEventListener("change", (event) => {
  // remove the active status on issues
  const issueItems = document.querySelectorAll(".map__issue_item");
  issueItems.forEach((item) => {
    item.classList.remove("map__active");
  });

  data = [...unfilteredData];
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

// Filter data using issue status
const issueStatus = document.querySelector(".map__issue-status");
issueStatus.addEventListener("click", (event) => {
  const value = event.target.textContent.toLowerCase();
  if (value == "open" || value == "resolved" || value == "review") {
    // check for values in the select
    data = [...unfilteredData];
    if (issueName.value) {
      data = data.filter((issue) =>
        issue.name.toLowerCase().includes(issueName.value)
      );
    }
    console.log(data, issueName);
    // filter by status
    data = data.filter((issue) => issue.status.includes(value));

    //remove all the markers
    removeAllMarkers();

    // add only the markers passing the condition
    data.forEach((item) => {
      let marker = L.marker([item.lat, item.long]).addTo(map);
      marker.bindPopup(`<b>${item.name}</b> <br> ${item.status}`);
    });
  }
});

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

// Generate random data
function generateDummyData() {
  const data = [];
  const issueNames = [
    "Graffiti",
    "Pothole",
    "Broken Streetlight",
    "Broken Sidewalk",
    "Abandoned Vehicle",
    "Stray Animals",
  ];

  const statuses = ["open", "review", "resolved"];

  for (let i = 0; i < 30; i++) {
    const randomIssueName =
      issueNames[Math.floor(Math.random() * issueNames.length)];
    const randomStatus = statuses[Math.floor(Math.random() * statuses.length)];
    const randomLat = getRandomLatitude();
    const randomLong = getRandomLongitude();

    data.push({
      name: randomIssueName,
      status: randomStatus,
      lat: randomLat,
      long: randomLong,
    });
  }

  return data;
}

// Generate a random latitude within the USA boundaries
function getRandomLatitude() {
  return Math.random() * (49.3457868 - 24.396308) + 24.396308;
}

// Generate a random longitude within the USA boundaries
function getRandomLongitude() {
  return Math.random() * (-66.9345704 - -125.0) + -125.0;
}
