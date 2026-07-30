import json
from pathlib import Path

SETTINGS_FILE = (
    Path(__file__).resolve().parent.parent
    / "config"
    / "settings.json"
)

DEFAULT_SETTINGS = {
    "default_country": "India",
    "default_city": "Delhi",
    "temperature_unit": "C",
    "wind_speed_unit": "km/h",
    "theme": "dark",
    "language": "en"
}


def load_settings():
    """
    Load settings safely.
    If the file is missing or invalid,
    recreate it using default settings.
    """

    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):

        save_settings(DEFAULT_SETTINGS)

        return DEFAULT_SETTINGS.copy()


def save_settings(settings):
    """
    Save settings to settings.json
    """

    SETTINGS_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
        json.dump(settings, file, indent=4)