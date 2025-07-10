import tkinter as tk
from colors import *
from pages.create_project_page import CreateProjectPage  # Ajoute ceci !

class HomePage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG)
        self.master = master  # Pour navigation
        self.create_ui()

    def create_ui(self):
        # --- Effet bento (shadow+carte) ---
        shadow = tk.Frame(self, bg=GAXD)
        shadow.place(relx=0.5, rely=0.52, anchor="center", width=430, height=345)
        
        # Carte centrale (glassmorphisme/neumorphisme soft)
        card = tk.Frame(self, bg=GW, highlightbackground=BF, highlightthickness=2, bd=0)
        card.place(relx=0.5, rely=0.5, anchor="center", width=410, height=330)
        
        # --- Logo (modifie le chemin de ton logo ici) ---
        try:
            logo = tk.PhotoImage(file="icone_boite.png")
            logo_label = tk.Label(card, image=logo, bg=GW, borderwidth=0)
            logo_label.image = logo
            logo_label.place(relx=0.5, y=56, anchor="center")
        except Exception:
            logo_label = tk.Label(card, text="🧩", font=("Arial", 38), bg=GW)
            logo_label.place(relx=0.5, y=56, anchor="center")
        
        # Titre
        title = tk.Label(card, text="Bienvenue sur l’Assistant CAO", font=("Segoe UI", 20, "bold"), fg=BF, bg=GW)
        title.place(relx=0.5, y=120, anchor="center")
        
        # Sous-titre
        subtitle = tk.Label(card, text="Innovation, Calculs, Dessin industriel.", font=("Segoe UI", 13), fg=VG, bg=GW)
        subtitle.place(relx=0.5, y=170, anchor="center")

        # --- Boutons principaux ---
        btn1 = tk.Button(
            card, text="Commencer un projet", font=("Segoe UI", 13, "bold"),
            fg=GW, bg=JV, activebackground=RV, activeforeground=GW,
            relief="flat", bd=0, width=18, height=2, cursor="hand2",
            command=self.start_project)
        btn1.place(relx=0.5, y=220, anchor="center")
        
        btn2 = tk.Button(
            card, text="Continuer un projet", font=("Segoe UI", 13, "bold"),
            fg=GW, bg=BA, activebackground=BA, activeforeground=GW,
            relief="flat", bd=0, width=18, height=2, cursor="hand2",
            command=self.continue_project)
        btn2.place(relx=0.5, y=270, anchor="center")

        # Version/Crédit
        version = tk.Label(card, text="v1.0 - © 2025 Jonathan", font=("Segoe UI", 9), fg=VG, bg=GW)
        version.place(relx=1.0, rely=1.0, anchor="se", x=-14, y=-9)

    def start_project(self):
        # Navigation vers la page de création de projet
        self.master.show_page(CreateProjectPage)
        
    def continue_project(self):
        # Navigation vers la page de sélection/chargement d’un projet existant
        print("Continuer un projet")
        # self.master.show_page(LoadProjectPage)  # À faire plus tard
