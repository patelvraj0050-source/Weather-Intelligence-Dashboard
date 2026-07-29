import tkinter as tk

from units.constants import BG_DARK, TEXT_MUTED, FOOTER_TEXT


class Footer(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG_DARK)

        self.pack(side="bottom", fill="x", pady=(0, 16))

        tk.Label(
            self,
            text=FOOTER_TEXT,
            bg=BG_DARK,
            fg=TEXT_MUTED,
            font=("Segoe UI", 9),
        ).pack()