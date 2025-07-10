# pieces/piece_cylindre.py

import tkinter as tk
from colors import *

class PieceCylindrePage(tk.Frame):
    def __init__(self, master, tech_sheet):
        super().__init__(master, bg=BG)
        self.master = master
        self.tech_sheet = tech_sheet

        # Titre
        title = tk.Label(
            self, text="Détail du cylindre",
            font=("Segoe UI", 20, "bold"),
            bg=BG, fg=BF
        )
        title.pack(pady=(24, 4))
        # Ligne jaune sous le titre
        tk.Frame(self, height=3, width=260, bg=JV).pack(pady=(0, 22))

        # Encadré infos
        info_frame = tk.Frame(self, bg=GW, bd=1, relief="ridge", padx=20, pady=15)
        info_frame.pack(padx=40, pady=10, fill="x")

        # Affichage harmonisé des infos techniques
        infos = [
            ("Diamètre interne (mm)", f"{tech_sheet['Diametre_m']*1000:.2f}"),
            ("Course (mm)",           f"{tech_sheet['Course_m']*1000:.2f}"),
            ("Épaisseur (mm)",        "2.00"),  # Adapter selon tech_sheet si dispo
            ("Matière",               "Acier"), # Adapter selon tech_sheet si dispo
            ("Température chaude (°C)", f"{tech_sheet['Temp_chaud_C']:.1f}"),
            ("Température froide (°C)", f"{tech_sheet['Temp_froid_C']:.1f}")
        ]
        for label, value in infos:
            row = tk.Frame(info_frame, bg=GW)
            row.pack(anchor="w", pady=4, fill="x")
            tk.Label(
                row, text=label + " : ", font=("Segoe UI", 13, "bold"),
                bg=GW, fg=BF, anchor="w"
            ).pack(side="left")
            tk.Label(
                row, text=value, font=("Segoe UI", 13),
                bg=GW, fg=JV, anchor="w"
            ).pack(side="left")

        # Bouton retour, bien large et centré
        tk.Button(
            self, text="Retour menu pièces", command=self.goto_back,
            bg=VO, fg=GW, font=("Segoe UI", 12, "bold"),
            activebackground=VG, activeforeground=JV,
            relief="raised", bd=2, padx=12, pady=4, cursor="hand2"
        ).pack(pady=32)

    def goto_back(self):
        from pages.parts_menu_page import PartsMenuPage
        self.master.show_page(PartsMenuPage, self.tech_sheet)
