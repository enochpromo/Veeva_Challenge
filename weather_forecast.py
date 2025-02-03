import requests
from datetime import datetime, timezone
from collections import defaultdict

def get_weather_forecast(zip_code, api_key):
    url = f"http://api.openweathermap.org/data/2.5/forecast?zip={zip_code},us&units=metric&appid={api_key}"
    
    response = requests.get(url)
    if response.status_code != 200:
        print("Error fetching data. Please check the ZIP code or API key.")
        return
    
    data = response.json()
    daily_forecast = defaultdict(lambda: {"high": float('-inf'), "low": float('inf'), "precip": 0})

    for entry in data["list"]:
        date = datetime.fromtimestamp(entry["dt"], timezone.utc).strftime('%m/%d/%Y')
        temp_min = entry["main"]["temp_min"]
        temp_max = entry["main"]["temp_max"]
        precip = entry.get("rain", {}).get("3h", 0)  # Rain volume for last 3 hours

        daily_forecast[date]["high"] = max(daily_forecast[date]["high"], temp_max)
        daily_forecast[date]["low"] = min(daily_forecast[date]["low"], temp_min)
        daily_forecast[date]["precip"] += precip  # Sum up precipitation for the day

    print("# Date       Temperature (High/Low)   Precipitation")
    for date, values in sorted(daily_forecast.items()):
        print(f"# {date}    {values['high']}/{values['low']}°C    {values['precip']} mm")

# Example usage:
api_key = "ecda433bc5c5315f9ed5e95e3a83c64e"  # Replace with your OpenWeatherMap API key
zip_code = "20769"  # Replace with the desired ZIP code
get_weather_forecast(zip_code, api_key)

