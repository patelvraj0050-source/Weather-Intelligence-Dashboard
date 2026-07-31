import tkinter as tk
from tkinter import ttk

from services.settings_service import (
    load_settings,
    save_settings
)

class SettingsWindow(tk.Toplevel):

    def __init__(self, master):
        super().__init__(master)

        self.title("Settings")

        self.geometry("350x450")

        self.resizable(False, False)

        self.city_var = tk.StringVar()

        self.country_var = tk.StringVar()

        self.temp_unit = tk.StringVar()

        self.theme_var = tk.StringVar()


        tk.Label(
            self,
            text="Default City"
        ).pack(anchor="w", padx=20, pady=(20, 5))

        tk.Entry(
            self,
            textvariable=self.city_var
        ).pack(fill="x", padx=20)

        tk.Label(
            self,
            text="Default Country"
        ).pack(anchor="w", padx=20, pady=(15, 5))

        tk.Entry(
            self,
            textvariable=self.country_var
        ).pack(fill="x", padx=20)


        tk.Label(
            self,
            text="Temperature Unit"
        ).pack(anchor="w", padx=20, pady=(15, 5))

        ttk.Combobox(
            self,
            textvariable=self.temp_unit,
            values=["C", "F"],
            state="readonly"
        ).pack(fill="x", padx=20)

        tk.Label(
            self,
            text="Theme"
        ).pack(anchor="w", padx=20, pady=(15, 5))

        ttk.Combobox(
            self,
            textvariable=self.theme_var,
            values=["dark", "light"],
            state="readonly"
        ).pack(fill="x", padx=20)

        tk.Button(
            self,
            text="Save",
            command=self.save
        ).pack(pady=20)

        settings = load_settings()  

        self.city_var.set(
            settings["default_city"]
        )

        self.country_var.set(
            settings["default_country"]
        )

        self.temp_unit.set(
            settings["temperature_unit"]
        )

        self.theme_var.set(
            settings["theme"]
        )


    def save(self):

        settings = load_settings()

        settings["default_city"] = self.city_var.get()

        settings["default_country"] = self.country_var.get()

        settings["temperature_unit"] = self.temp_unit.get()

        settings["theme"] = self.theme_var.get()

        save_settings(settings)

        self.master.reload_settings()

        self.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    SettingsWindow(root)

    root.mainloop()