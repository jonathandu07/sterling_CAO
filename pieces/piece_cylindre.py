# pieces/piece_cylindre.py
import tkinter as tk
from colors import *
from PIL import Image, ImageTk
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

from calculs.cylindre import CylindreStirling
from plans.plans_cylindre import plot_cylindre

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
        tk.Frame(self, height=3, width=260, bg=JV).pack(pady=(0, 22))

        # Création de l'objet cylindre à partir des données tech_sheet
        self.cylindre = CylindreStirling(
            diametre_m=tech_sheet['Diametre_m'],
            course_m=tech_sheet['Course_m'],
            epaisseur_m=tech_sheet.get('Epaisseur_m', 0.002),
            matiere=tech_sheet.get('Matiere', 'Acier'),
            densite_kg_m3=tech_sheet.get('Densite_kg_m3', 7850),
            rugosite_um=tech_sheet.get('Rugosite_um', 0.8),
            etat_surface=tech_sheet.get('Etat_surface', 'Usinage fin'),
            Th=tech_sheet['Temp_chaud_C'] + 273.15,
            Tc=tech_sheet['Temp_froid_C'] + 273.15,
            nb_vis=tech_sheet.get('Nb_vis', 6),
            dim_vis_iso=tech_sheet.get('Dim_vis_iso', 'M6'),
            entraxe_vis_pct=tech_sheet.get('Entraxe_vis_pct', 0.85),
            limite_rupture_MPa=tech_sheet.get('Limite_rupture_MPa', 700)
        )

        # Cadre infos techniques
        info_frame = tk.Frame(self, bg=GW, bd=1, relief="ridge", padx=20, pady=15)
        info_frame.pack(padx=40, pady=10, fill="x")

        # Récupération et affichage dynamique des infos calculées
        infos_dict = self.cylindre.to_dict()
        for label, value in infos_dict.items():
            row = tk.Frame(info_frame, bg=GW)
            row.pack(anchor="w", pady=3, fill="x")
            tk.Label(
                row, text=label + " : ", font=("Segoe UI", 13, "bold"),
                bg=GW, fg=BF, anchor="w"
            ).pack(side="left")
            tk.Label(
                row, text=str(value), font=("Segoe UI", 13),
                bg=GW, fg=JV, anchor="w"
            ).pack(side="left")

        # Génération du plan du cylindre
        self.plan_path = "plan_cylindre.png"
        plot_cylindre(self.cylindre, self.plan_path)

        # Affichage du plan
        if os.path.exists(self.plan_path):
            image = Image.open(self.plan_path)
            image = image.resize((800, 400), Image.Resampling.LANCZOS)
            self.photo = ImageTk.PhotoImage(image)
            tk.Label(self, image=self.photo, bg=BG).pack(pady=15)
        else:
            tk.Label(self, text="Erreur : le plan n’a pas pu être généré.", fg=RV, bg=BG).pack(pady=15)

        # Boutons
        btn_frame = tk.Frame(self, bg=BG)
        btn_frame.pack(pady=20)

        tk.Button(
            btn_frame, text="Retour menu pièces", command=self.goto_back,
            bg=VO, fg=GW, font=("Segoe UI", 12, "bold"),
            activebackground=VG, activeforeground=JV,
            relief="raised", bd=2, padx=12, pady=4, cursor="hand2"
        ).pack(side="left", padx=20)

        tk.Button(
            btn_frame, text="Exporter PDF", command=self.generate_pdf,
            bg=JV, fg=BF, font=("Segoe UI", 12, "bold"),
            relief="raised", bd=2, padx=12, pady=4, cursor="hand2"
        ).pack(side="left", padx=20)

    def generate_pdf(self):
        pdf_path = "cylindre_technique.pdf"
        c = canvas.Canvas(pdf_path, pagesize=A4)
        width, height = A4

        c.setFont("Helvetica-Bold", 16)
        c.drawString(30, height - 50, "Fiche technique du cylindre")

        # Texte infos techniques dynamiques
        c.setFont("Helvetica", 12)
        y = height - 90
        infos_dict = self.cylindre.to_dict()
        for label, value in infos_dict.items():
            line = f"{label} : {value}"
            c.drawString(30, y, line)
            y -= 18
            if y < 100:
                c.showPage()
                y = height - 50
                c.setFont("Helvetica", 12)

        # Insérer l'image du plan
        if os.path.exists(self.plan_path):
            c.drawImage(self.plan_path, 30, y - 300, width=550, height=250, preserveAspectRatio=True, mask='auto')

        c.save()
        print(f"PDF généré : {pdf_path}")

    def goto_back(self):
        from pages.parts_menu_page import PartsMenuPage
        self.master.show_page(PartsMenuPage, self.tech_sheet)
