# main.py
import tkinter as tk
from colors import *
from pages.home_page import HomePage

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Assistant CAO")
        self.geometry("700x500")
        self.configure(bg=BG)
        self.resizable(False, False)
        self.current_frame = None

        # Pour charger la première page (Accueil)
        self.show_page(HomePage)

    def show_page(self, PageClass):
        # Détruit la page courante si elle existe
        if self.current_frame:
            self.current_frame.destroy()
        # Affiche la nouvelle page
        self.current_frame = PageClass(self)
        self.current_frame.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
