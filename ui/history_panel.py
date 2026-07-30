import tkinter as tk
from units.constants import BG_CARD, TEXT_MAIN


class HistoryPanel(tk.Frame):

    def __init__(self, master):
        super().__init__(master, bg=BG_CARD)

        self.pack(fill="x", padx=24, pady=(0, 16))

        tk.Label(
            self,
            text="Recent Searches",
            bg=BG_CARD,
            fg=TEXT_MAIN,
            font=("Segoe UI", 12, "bold"),
        ).pack(anchor="w", padx=16, pady=(12, 8))

        self.button_frame = tk.Frame(self, bg=BG_CARD)
        self.button_frame.pack(fill="x", padx=16, pady=(0, 12))