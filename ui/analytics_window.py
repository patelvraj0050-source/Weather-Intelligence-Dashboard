import tkinter as tk

from database.database_service import (
    get_total_searches,
    get_most_searched_city,
    get_total_countries,
)


class AnalyticsWindow(tk.Toplevel):

    def __init__(self, master):
        super().__init__(master)

        self.title("📊 Weather Analytics")

        self.geometry("550x500")

        self.resizable(False, False)

        title = tk.Label(
            self,
            text="📊 Weather Analytics",
            font=("Segoe UI", 18, "bold")
        )

        title.pack(pady=20)

        self.build_card(
            "🔍 Total Searches",
            str(get_total_searches())
        )

        city = get_most_searched_city()

        if city:
            value = f"{city[0]}\n({city[1]} searches)"
        else:
            value = "No Data"

        self.build_card(
            "🏙 Most Searched City",
            value
        )

        self.build_card(
            "🌍 Countries Searched",
            str(get_total_countries())
        )

    def build_card(self, title, value):

        frame = tk.Frame(
            self,
            relief="groove",
            bd=2
        )

        frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        tk.Label(
            frame,
            text=title,
            font=("Segoe UI", 12, "bold")
        ).pack(anchor="w", padx=15, pady=(10,5))

        tk.Label(
            frame,
            text=value,
            font=("Segoe UI", 18)
        ).pack(pady=(0,15))