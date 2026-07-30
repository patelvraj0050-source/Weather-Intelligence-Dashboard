import json
from pathlib import Path

# Path to config/settings.json
SETTINGS_FILE = (
    Path(__file__).resolve().parent.parent
    / "config"
    / "settings.json"
)


def load_settings():
    """
    Load application settings from settings.json.
    Returns a dictionary.
    """
    with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_settings(settings):
    """
    Save application settings to settings.json.
    """
    with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
        json.dump(settings, file, indent=4)