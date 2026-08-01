import tkinter as tk


class AnalyticsPanel(tk.Frame):

    def __init__(self, master):
        super().__init__(master)

        self.pack(fill="x", padx=24, pady=(10, 10))

        tk.Label(
            self,
            text="📊 Search Analytics",
            font=("Segoe UI", 14, "bold")
        ).pack(anchor="w")

        self.total_label = tk.Label(self, text="")
        self.total_label.pack(anchor="w", pady=(8, 0))

        self.city_label = tk.Label(self, text="")
        self.city_label.pack(anchor="w")

        self.country_label = tk.Label(self, text="")
        self.country_label.pack(anchor="w")