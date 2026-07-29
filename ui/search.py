import tkinter as tk
from tkinter import ttk

from units.constants import (
    BG_DARK,
    TEXT_MUTED,
    COUNTRIES,
)


class SearchPanel(tk.Frame):
    def __init__(self, parent, search_callback, country_callback):
        super().__init__(parent, bg=BG_DARK)

        self.pack(fill="x", padx=24, pady=(4, 16))

        # ---------- Country ----------
        country_row = tk.Frame(self, bg=BG_DARK)
        country_row.pack(fill="x", pady=(0, 8))

        tk.Label(
            country_row,
            text="Country",
            bg=BG_DARK,
            fg=TEXT_MUTED,
            font=("Segoe UI", 9),
        ).pack(anchor="w")

        self.country_var = tk.StringVar()

        self.country_box = ttk.Combobox(
            country_row,
            textvariable=self.country_var,
            values=[name for name, code in COUNTRIES],
            style="Search.TCombobox",
            state="readonly",
            font=("Segoe UI", 12),
        )

        self.country_box.pack(fill="x", ipady=4, pady=(2, 0))
        self.country_box.bind("<<ComboboxSelected>>", country_callback)

        # ---------- City ----------
        city_row = tk.Frame(self, bg=BG_DARK)
        city_row.pack(fill="x")

        tk.Label(
            city_row,
            text="City",
            bg=BG_DARK,
            fg=TEXT_MUTED,
            font=("Segoe UI", 9),
        ).pack(anchor="w")

        city_input_row = tk.Frame(city_row, bg=BG_DARK)
        city_input_row.pack(fill="x", pady=(2, 0))

        self.city_var = tk.StringVar()

        self.city_box = ttk.Combobox(
            city_input_row,
            textvariable=self.city_var,
            values=[],
            style="Search.TCombobox",
            state="disabled",
            font=("Segoe UI", 12),
        )

        self.city_box.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=6,
        )

        self.city_box.bind("<Return>", lambda e: search_callback())
        self.city_box.bind("<<ComboboxSelected>>", lambda e: search_callback())

        tk.Button(
            city_input_row,
            text="Search",
            bg="#4f9dff",
            fg="#0b0f18",
            activebackground="#2f65b8",
            activeforeground="white",
            relief="flat",
            font=("Segoe UI", 11, "bold"),
            padx=16,
            cursor="hand2",
            command=search_callback,
        ).pack(side="left", padx=(8, 0))