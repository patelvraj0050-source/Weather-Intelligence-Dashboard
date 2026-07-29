import tkinter as tk

from units.constants import BG_CARD, ACCENT, TEXT_MAIN, TEXT_SUB, TEXT_MUTED


class WeatherCard(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG_CARD)

        self.pack(fill="x", padx=24, pady=(0, 16))

        inner = tk.Frame(self, bg=BG_CARD)
        inner.pack(fill="x", padx=24, pady=24)

        self.city_label = tk.Label(
            inner,
            text="",
            bg=BG_CARD,
            fg=TEXT_MAIN,
            font=("Segoe UI", 16, "bold"),
        )
        self.city_label.pack(anchor="w")

        self.condition_label = tk.Label(
            inner,
            text="",
            bg=BG_CARD,
            fg=TEXT_SUB,
            font=("Segoe UI", 11),
        )
        self.condition_label.pack(anchor="w", pady=(2, 12))

        row = tk.Frame(inner, bg=BG_CARD)
        row.pack(fill="x")

        self.icon_label = tk.Label(
            row,
            text="☀",
            bg=BG_CARD,
            fg=ACCENT,
            font=("Segoe UI", 48),
        )
        self.icon_label.pack(side="left")

        self.temp_label = tk.Label(
            row,
            text="",
            bg=BG_CARD,
            fg=TEXT_MAIN,
            font=("Segoe UI", 46, "bold"),
        )
        self.temp_label.pack(side="left", padx=(16, 0))

        self.feels_label = tk.Label(
            inner,
            text="",
            bg=BG_CARD,
            fg=TEXT_MUTED,
            font=("Segoe UI", 10),
        )
        self.feels_label.pack(anchor="w", pady=(6, 0))