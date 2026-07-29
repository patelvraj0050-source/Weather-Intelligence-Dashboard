import tkinter as tk

from units.constants import BG_DARK, BG_CARD, TEXT_MAIN, TEXT_MUTED


class StatsPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG_DARK)

        self.pack(fill="x", padx=24, pady=(0, 16))

        self.columnconfigure((0, 1, 2, 3), weight=1)

        self.stat_widgets = {}

        labels = [
            ("High", "high", "°"),
            ("Low", "low", "°"),
            ("Humidity", "humidity", "%"),
            ("Wind", "wind", " km/h"),
        ]

        for col, (title, key, suffix) in enumerate(labels):
            box = tk.Frame(self, bg=BG_CARD)
            box.grid(row=0, column=col, sticky="nsew", padx=4)

            tk.Label(
                box,
                text=title,
                bg=BG_CARD,
                fg=TEXT_MUTED,
                font=("Segoe UI", 9),
            ).pack(pady=(10, 2))

            value = tk.Label(
                box,
                text="--",
                bg=BG_CARD,
                fg=TEXT_MAIN,
                font=("Segoe UI", 14, "bold"),
            )

            value.pack(pady=(0, 10))

            self.stat_widgets[key] = (value, suffix)