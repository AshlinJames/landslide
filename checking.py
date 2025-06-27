import requests

# Define API endpoint
endpoint = "https://api.open-meteo.com/v1/forecast"

# Define parameters correctly
params = {
    "latitude": 51.5074,  # Example: London (Update for your location)
    "longitude": -0.1278,
    "current": "temperature_2m,relative_humidity_2m,precipitation,dewpoint_2m,windspeed_10m",
    "hourly": "temperature_2m,relative_humidity_2m,precipitation,dewpoint_2m,windspeed_10m,soil_moisture_0_to_7cm",
    "timezone": "auto"  # Removed the problematic elevation parameter
}

# Fetch data
response = requests.get(endpoint, params=params)

# Check for errors
if response.status_code == 200:
    data = response.json()

    # Extract weather data
    current_weather = data.get("current", {})
    temperature = current_weather.get("temperature_2m", "N/A")
    humidity = current_weather.get("relative_humidity_2m", "N/A")
    precipitation = current_weather.get("precipitation", "N/A")
    dewpoint = current_weather.get("dewpoint_2m", "N/A")
    windspeed = current_weather.get("windspeed_10m", "N/A")
    elevation = data.get("elevation", "N/A")

    # Display extracted data
    print(f"🌡️ Temperature: {temperature}°C")
    print(f"💧 Humidity: {humidity}%")
    print(f"🌧️ Precipitation: {precipitation} mm")
    print(f"❄️ Dew Point: {dewpoint}°C")
    print(f"🌪️ Wind Speed: {windspeed} m/s")
    print(f"📏 Elevation: {elevation} m")
else:
    print(f"❌ Failed to fetch data. Status Code: {response.status_code}")
    print(f"Response: {response.text}")  # Print API error details