

import threading
import tkinter as tk
from tkinter import ttk
from datetime import datetime

from services.weather_api import fetch_weather
from ui.footer import Footer
from ui.header import Header
from ui.weather_card import WeatherCard
from ui.stats import StatsPanel
from ui.search import SearchPanel
from units.constants import (
    BG_DARK,
    BG_CARD,
    BG_CARD_HOVER,
    ACCENT,
    ACCENT_SOFT,
    TEXT_MAIN,
    TEXT_SUB,
    TEXT_MUTED,
    GOOD,
    WARN,
    BAD,
    COUNTRIES,
    CITY_SUGGESTIONS,
    FOOTER_TEXT,
)
from services.settings_service import load_settings
from logs.logging_service import logger

from database.database_service import (
    initialize_database,
    save_search,
    get_recent_searches,
    add_favorite,
    get_favorites,
)

from ui.history_panel import HistoryPanel
from ui.favourites_panel import FavoritesPanel
from ui.settings_window import SettingsWindow


class WeatherApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.settings = load_settings()
        self.title("Weather • Static Demo")
        self.geometry("500x900")
        self.minsize(480, 850)
        self.configure(bg=BG_DARK)
        self.resizable(True, True)
        self._build_style()
        header = Header(self)
        
        self.updated_label = header.updated_label

        self.settings_button = tk.Button(
            self,
            text="⚙ Settings",
            command=self.open_settings
        )

        self.settings_button.pack(
            anchor="e",
            padx=24,
            pady=(0, 10)
        )
        
        search_panel = SearchPanel(
            self,
            self.search,
            self._on_country_selected,
        )

        self.country_var = search_panel.country_var
        self.country_box = search_panel.country_box

        self.city_var = search_panel.city_var
        self.city_box = search_panel.city_box
        
        card = WeatherCard(self)
        

        self.city_label = card.city_label
        self.condition_label = card.condition_label
        self.icon_label = card.icon_label
        self.temp_label = card.temp_label
        self.feels_label = card.feels_label

        self.favorite_button = tk.Button(
            self,
            text="⭐ Add to Favorites",
            command=self.add_current_to_favorites
        )

        self.favorite_button.pack(pady=5)
        
        stats = StatsPanel(self)
        self.stat_widgets = stats.stat_widgets

        favorites = FavoritesPanel(self)
        self.favorites_panel = favorites

        history = HistoryPanel(self)
        self.history_panel = history


        
        Footer(self)
        self.update_favorites()
        self.update_history()

        self.country_var.set(self.settings["default_country"])
        self._on_country_selected()

        self.city_var.set(self.settings["default_city"])

        self.current_city = None
        self.current_country = None

        self.search()

        

    def _build_style(self):
        self.option_add("*Font", "Segoeui 11")
        style = ttk.Style(self)
        style.theme_use("default")
        style.configure(
            "Search.TCombobox",
            fieldbackground=BG_CARD,
            background=BG_CARD,
            foreground=TEXT_MAIN,
            arrowcolor=TEXT_MAIN,
            bordercolor=BG_CARD,
            lightcolor=BG_CARD,
            darkcolor=BG_CARD,
        )

    def _build_header(self):
        header = tk.Frame(self, bg=BG_DARK)
        header.pack(fill="x", padx=24, pady=(24, 8))

        tk.Label(
            header, text="Weather", bg=BG_DARK, fg=TEXT_MAIN,
            font=("Segoeui", 22, "bold")
        ).pack(anchor="w")

        self.updated_label = tk.Label(
            header, text="", bg=BG_DARK, fg=TEXT_MUTED, font=("Segoeui", 9)
        )
        self.updated_label.pack(anchor="w", pady=(2, 0))


    def _on_country_selected(self, event=None):
        name = self.country_var.get()
        code = dict(COUNTRIES).get(name)
        cities = CITY_SUGGESTIONS.get(code, [])
        self.city_box.config(values=cities, state="normal")
        self.city_var.set("")
        self.city_box.focus_set()

    def _build_card(self):
        self.card = tk.Frame(self, bg=BG_CARD)
        self.card.pack(fill="x", padx=24, pady=(0, 16))

        inner = tk.Frame(self.card, bg=BG_CARD)
        inner.pack(fill="x", padx=24, pady=24)

        self.city_label = tk.Label(
            inner, text="", bg=BG_CARD, fg=TEXT_MAIN, font=("Segoeui", 16, "bold")
        )
        self.city_label.pack(anchor="w")

        self.condition_label = tk.Label(
            inner, text="", bg=BG_CARD, fg=TEXT_SUB, font=("Segoeui", 11)
        )
        self.condition_label.pack(anchor="w", pady=(2, 12))

        row = tk.Frame(inner, bg=BG_CARD)
        row.pack(fill="x")

        self.icon_label = tk.Label(
            row, text="☀", bg=BG_CARD, fg=ACCENT, font=("Segoeui", 48)
        )
        self.icon_label.pack(side="left")

        self.temp_label = tk.Label(
            row, text="", bg=BG_CARD, fg=TEXT_MAIN, font=("Segoeui", 46, "bold")
        )
        self.temp_label.pack(side="left", padx=(16, 0))

        self.feels_label = tk.Label(
            inner, text="", bg=BG_CARD, fg=TEXT_MUTED, font=("Segoeui", 10)
        )
        self.feels_label.pack(anchor="w", pady=(6, 0))

    
    def search(self):

        logger.info(
            f"Searching weather | Country: {self.country_var.get()} | City: {self.city_var.get()}"
        )

        query = self.city_var.get().strip()
        country_name = self.country_var.get().strip()
        if not country_name:
            self.show_loading("")
            self.condition_label.config(text="Pick a country first")
            return
        if not query:
            return
        country_code = dict(COUNTRIES).get(country_name)
        self.show_loading(query)
        threading.Thread(
            target=self._fetch_worker, args=(query, country_code), daemon=True
        ).start()

    def _fetch_worker(self, query, country_code):
        try:
            data = fetch_weather(query, country_code)

            logger.info("Weather data fetched successfully.")

            self.after(0, self.show_city, data)

        except Exception as e:

            logger.exception(f"Weather fetch failed: {e}")

            self.after(0, self.show_not_found, query)


    
    def show_loading(self, query):
        self.city_label.config(text=f"Loading {query}...", fg=TEXT_MAIN)
        self.condition_label.config(text="Fetching live data from Open-Meteo")
        self.icon_label.config(text="⏳")
        self.temp_label.config(text="--")
        self.feels_label.config(text="")
        for widget, _ in self.stat_widgets.values():
            widget.config(text="--")

    def show_city(self, data):
        self.city_var.set(data["resolved_name"])

        save_search(
            data["resolved_name"],
            self.country_var.get()
        )

        self.current_city = data["resolved_name"]
        self.current_country = self.country_var.get()


        self.update_history()


        self.city_label.config(text=data["resolved_name"], fg=TEXT_MAIN)
        self.condition_label.config(text=data["condition"])
        self.icon_label.config(text=data["icon"])
        self.temp_label.config(text=f"{data['temp']}°C")
        self.feels_label.config(text=f"Feels like {data['feels']}°C")

        for key, (widget, suffix) in self.stat_widgets.items():
            widget.config(text=f"{data[key]}{suffix}")

        now = datetime.now().strftime("%A, %d %b — %I:%M %p")
        self.updated_label.config(text=f"Last updated: {now} (live via Open-Meteo)")

    def update_history(self):
    
            for widget in self.history_panel.button_frame.winfo_children():
                widget.destroy()
    
            recent = get_recent_searches()
    
            if not recent:
    
                tk.Label(
                    self.history_panel.button_frame,
                    text="No searches yet",
                    bg=BG_CARD,
                    fg=TEXT_SUB,
                ).pack(anchor="w")
    
                return
    
            for city, country, _ in recent:
    
                tk.Button(
                    self.history_panel.button_frame,
                    text=f"{city}, {country}",
                    command=lambda c=city: self.search_from_history(c),
                ).pack(fill="x", pady=2)
    
    

    def update_favorites(self):
    
            for widget in self.favorites_panel.button_frame.winfo_children():
                widget.destroy()
    
            favorites = get_favorites()
    
            if not favorites:
    
                tk.Label(
                    self.favorites_panel.button_frame,
                    text="No favorite cities",
                    bg=BG_CARD,
                    fg=TEXT_SUB,
                ).pack(anchor="w")
    
                return
    
            for city, country in favorites:
    
                tk.Button(
                    self.favorites_panel.button_frame,
                    text=f"⭐ {city}, {country}",
                    command=lambda c=city: self.search_from_history(c),
                ).pack(fill="x", pady=2)

    def add_current_to_favorites(self):

        if self.current_city is None:
            return

        add_favorite(
            self.current_city,
            self.current_country
        )

        self.update_favorites()

    def reload_settings(self):

        self.settings = load_settings()

        self.country_var.set(
            self.settings["default_country"]
        )

        self._on_country_selected()

        self.city_var.set(
            self.settings["default_city"]
        )

        self.search()
    
    
    def search_from_history(self, city):

        self.city_var.set(city)

        self.search()

    def open_settings(self):

        SettingsWindow(self)


    def show_not_found(self, query):
        self.city_label.config(text=f'"{query}" not found', fg=BAD)
        self.condition_label.config(text="Check spelling or your internet connection")
        self.icon_label.config(text="✕")
        self.temp_label.config(text="--")
        self.feels_label.config(text="")
        for widget, _ in self.stat_widgets.values():
            widget.config(text="--")


if __name__ == "__main__":
    logger.info("Application started.")

    initialize_database()

    app = WeatherApp()

    app.mainloop()
