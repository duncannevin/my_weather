// app.js
const apiKey = "YOUR_API_KEY"; // Replace with your OpenWeatherMap API key

// Initialize the map
const map = L.map("map").setView([37.7749, -122.4194], 5); // Centered on San Francisco

// Add OpenStreetMap tiles
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: 19,
  attribution: "&copy; OpenStreetMap contributors"
}).addTo(map);

// Add a click event listener to the map
map.on("click", async (e) => {
  const lat = e.latlng.lat;
  const lon = e.latlng.lng;

  try {
    const weatherData = await fetchWeatherData(lat, lon);
    const forecastData = await fetchForecastData(lat, lon);
    displayWeatherData(weatherData, lat, lon);
    displayForecastData(forecastData);
  } catch (error) {
    console.error("Error fetching weather data:", error);
    document.getElementById("weather-data").innerHTML = `<p>Error fetching weather data. Please try again.</p>`;
    document.getElementById("forecast-data").innerHTML = "";
  }
});


// Fetch weather data from OpenWeatherMap API
async function fetchWeatherData(lat, lon) {
  const url = '/weather';
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      lat,
      lon,
      units: "imperial"
    })});

  if (!response.ok) {
    throw new Error("Failed to fetch weather data");
  }

  return await response.json();
}

// Fetch 10-day forecast data
async function fetchForecastData(lat, lon) {
  const url = '/weather/forecast?lat=' + lat + '&lon=' + lon + '&units=imperial&cnt=10';
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error("Failed to fetch forecast data");
  }
  return await response.json();
}

// Display weather data on the page
function displayWeatherData(data) {
  const weatherDiv = document.getElementById("weather-data");
  weatherDiv.innerHTML = `
    <h3>Weather in ${data.name || "Selected Location"}</h3>
    <p>Coordinates: ${data.coord.lat.toFixed(2)}, ${data.coord.lon.toFixed(2)}</p>
    <p>Description: ${data.weather[0].description}</p>
    <p>Temperature: ${data.main.temp} °F</p>
    <p>Humidity: ${data.main.humidity}%</p>
    <p>Wind Speed: ${data.wind.speed} mph</p>
  `;
}

// Display 10-day forecast data
function displayForecastData(data) {
  const forecastDiv = document.getElementById("forecast-data");
  let forecastHTML = "<h3>10-Day Forecast</h3><ul>";

  data.list.forEach((day) => {
    const date = new Date(day.dt * 1000).toLocaleDateString();
    forecastHTML += `
      <li>
        <p><strong>${date}</strong></p>
        <p>Temperature: ${day.temp.day} °F</p>
        <p>Weather: ${day.weather[0].description}</p>
        <p>Humidity: ${day.humidity}%</p>
      </li>
    `;
  });

  forecastHTML += "</ul>";
  forecastDiv.innerHTML = forecastHTML;
}
