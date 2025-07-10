import tkinter as tk
from colors import *
from PIL import Image, ImageTk
import os

from calculs.cylindre import CylindreStirling
from plans.plans_cylindre import plot_cylindre

class PieceCylindrePage(tk.Frame):
    def __init__(self, master, tech_sheet):
        super().__init__(master, bg=BG)
        self.master = master
        self.tech_sheet = tech_sheet

        tk.Label(self, text="Détail du cylindre", font=("Segoe UI", 20, "bold"), bg=BG, fg=BF).pack(pady=18)
        
        infos = [
            f"Diamètre interne (mm) : {tech_sheet['Diametre_m']*1000:.2f}",
            f"Course (mm) : {tech_sheet['Course_m']*1000:.2f}",
            f"Épaisseur (mm) : 2.00",  # À adapter si dispo dans tech_sheet
            f"Matière : Acier",        # Idem
            f"Température chaude (°C) : {tech_sheet['Temp_chaud_C']:.1f}",
            f"Température froide (°C) : {tech_sheet['Temp_froid_C']:.1f}"
        ]
        for info in infos:
            tk.Label(self, text=info, font=("Segoe UI", 13), bg=BG, fg=BF).pack(anchor="w", padx=24, pady=2)

        # Création de l'objet cylindre avec les paramètres par défauts manquants
        cylindre = CylindreStirling(
            diametre_m=tech_sheet['Diametre_m'],
            course_m=tech_sheet['Course_m'],
            epaisseur_m=0.002,  # Exemple d’épaisseur fixe ou à récupérer dans tech_sheet
            matiere="Acier",
            densite_kg_m3=7850,
            rugosite_um=0.8,
            etat_surface="Usinage fin",
            Th=tech_sheet['Temp_chaud_C'] + 273.15,
            Tc=tech_sheet['Temp_froid_C'] + 273.15,
            nb_vis=6,
            dim_vis_iso="M6",
            entraxe_vis_pct=0.85,
            limite_rupture_MPa=700
        )
        plan_path = "plan_cylindre.png"
        plot_cylindre(cylindre, plan_path)

        # Affichage du plan dans la page
        if os.path.exists(plan_path):
            image = Image.open(plan_path)
            image = image.resize((500, 250))  # Ajuste la taille selon besoin
            self.photo = ImageTk.PhotoImage(image)
            tk.Label(self, image=self.photo, bg=BG).pack(pady=15)
        else:
            tk.Label(self, text="Erreur : le plan n’a pas pu être généré.", fg="red", bg=BG).pack()

        tk.Button(self, text="Retour menu pièces", command=self.goto_back, bg=VO, fg=GW).pack(pady=35)

    def goto_back(self):
        from pages.parts_menu_page import PartsMenuPage
        self.master.show_page(PartsMenuPage, self.tech_sheet)
