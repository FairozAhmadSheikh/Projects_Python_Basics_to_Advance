import requests

API_KEY = "your_openweather_api_key"  # Replace with your API key
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather(city):
    """Fetch weather data for a given city."""
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if data["cod"] == 200:
        temp = data["main"]["temp"]
        weather = data["weather"][0]["description"]
        print(f"Weather in {city}: {weather}, {temp}°C")
    else:
        print("City not found. Please try again.")

# Get city from user
city_name = input("Enter city name: ")
get_weather(city_name)
