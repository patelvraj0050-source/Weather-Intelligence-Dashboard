import tkinter as tk

from units.constants import (
    BG_DARK,
    TEXT_MAIN,
    TEXT_MUTED,
)

class Header(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG_DARK)

        self.pack(fill="x", padx=24, pady=(24, 8))

        tk.Label(
            self,
            text="Weather",
            bg=BG_DARK,
            fg=TEXT_MAIN,
            font=("Segoe UI", 22, "bold"),
        ).pack(anchor="w")

        self.updated_label = tk.Label(
            self,
            text="",
            bg=BG_DARK,
            fg=TEXT_MUTED,
            font=("Segoe UI", 9),
        )

        self.updated_label.pack(anchor="w", pady=(2, 0))