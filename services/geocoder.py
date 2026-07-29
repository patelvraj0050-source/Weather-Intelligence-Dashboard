import json
import urllib.parse
import urllib.request


def geocode(city, country_code=None):
    """
    Convert a city name into latitude and longitude
    using the Open-Meteo Geocoding API.
    """

    base = "https://geocoding-api.open-meteo.com/v1/search"

    attempts = []

    if country_code:
        attempts.append({
            "name": city,
            "country": country_code,
            "count": 1
        })

    attempts.append({
        "name": city,
        "count": 1
    })

    for params in attempts:

        geo_url = f"{base}?{urllib.parse.urlencode(params)}"

        req = urllib.request.Request(
            geo_url,
            headers={"User-Agent": "curl/8.0"}
        )

        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())

        results = data.get("results")

        if results:
            top = results[0]

            label_parts = [top["name"]]

            if top.get("admin1"):
                label_parts.append(top["admin1"])

            if top.get("country"):
                label_parts.append(top["country"])

            return (
                top["latitude"],
                top["longitude"],
                ", ".join(label_parts)
            )

    raise ValueError(f"City not found: {city}")