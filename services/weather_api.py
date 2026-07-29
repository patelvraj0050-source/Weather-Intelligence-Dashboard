import json
import urllib.parse
import urllib.request

from services.geocoder import geocode
from units.constants import WMO_CODES




def icon_for(description):
    desc = description.lower()

    if "thunder" in desc:
        return "⛈"

    if "snow" in desc or "sleet" in desc or "ice" in desc:
        return "❄"

    if "rain" in desc or "drizzle" in desc or "shower" in desc:
        return "🌧"

    if "fog" in desc or "mist" in desc or "haze" in desc:
        return "🌫"

    if "overcast" in desc:
        return "☁"

    if "cloud" in desc:
        return "⛅"

    if "clear" in desc or "sunny" in desc:
        return "☀"

    return "🌤"


def fetch_weather(city, country_code=None):

    lat, lon, resolved_name = geocode(city, country_code)

    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,apparent_temperature,relative_humidity_2m,wind_speed_10m,weather_code",
        "daily": "temperature_2m_max,temperature_2m_min",
        "timezone": "auto",
    }

    url = f"https://api.open-meteo.com/v1/forecast?{urllib.parse.urlencode(params)}"

    req = urllib.request.Request(
        url,
        headers={"User-Agent": "curl/8.0"}
    )

    with urllib.request.urlopen(req, timeout=10) as resp:
        raw = json.loads(resp.read().decode())

    current = raw["current"]
    daily = raw["daily"]

    code = current["weather_code"]

    description = WMO_CODES.get(code, "Unknown")

    return {
        "resolved_name": resolved_name,
        "temp": round(current["temperature_2m"]),
        "feels": round(current["apparent_temperature"]),
        "condition": description,
        "icon": icon_for(description),
        "humidity": round(current["relative_humidity_2m"]),
        "wind": round(current["wind_speed_10m"]),
        "high": round(daily["temperature_2m_max"][0]),
        "low": round(daily["temperature_2m_min"][0]),
    }