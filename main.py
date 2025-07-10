# main.py
import tkinter as tk
from colors import *
from pages.home_page import HomePage

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Assistant CAO")
        self.geometry("900x700")           # Taille adaptée au confort visuel
        self.configure(bg=BG)
        self.resizable(True, True)         # Autorise le redimensionnement
        self.current_frame = None

        self.show_page(HomePage)

    def show_page(self, PageClass, *args, **kwargs):
        """Affiche la page demandée (remplace l'actuelle)."""
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = PageClass(self, *args, **kwargs)
        self.current_frame.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
