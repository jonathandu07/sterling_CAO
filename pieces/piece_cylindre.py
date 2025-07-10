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

        # Cadre infos techniques
        info_frame = tk.Frame(self, bg=GW, bd=1, relief="ridge", padx=20, pady=15)
        info_frame.pack(padx=40, pady=10, fill="x")

        # Infos à afficher (ajoute ici plus d'infos si disponibles dans tech_sheet)
        infos = [
            ("Diamètre interne (mm)", f"{tech_sheet['Diametre_m']*1000:.2f}"),
            ("Course (mm)",           f"{tech_sheet['Course_m']*1000:.2f}"),
            ("Épaisseur (mm)",        "2.00"),  # Adapter si présent dans tech_sheet
            ("Matière",               "Acier"),
            ("Densité (kg/m³)",       "7850"),
            ("Rugosité (µm)",         "0.8"),
            ("État surface",          "Usinage fin"),
            ("Température chaude (°C)", f"{tech_sheet['Temp_chaud_C']:.1f}"),
            ("Température froide (°C)", f"{tech_sheet['Temp_froid_C']:.1f}"),
            ("Nb vis",                "6"),
            ("Dimension vis ISO",     "M6"),
            ("Entraxe vis (%)",       "85"),
            ("Limite rupture (MPa)",  "700"),
        ]

        for label, value in infos:
            row = tk.Frame(info_frame, bg=GW)
            row.pack(anchor="w", pady=3, fill="x")
            tk.Label(
                row, text=label + " : ", font=("Segoe UI", 13, "bold"),
                bg=GW, fg=BF, anchor="w"
            ).pack(side="left")
            tk.Label(
                row, text=value, font=("Segoe UI", 13),
                bg=GW, fg=JV, anchor="w"
            ).pack(side="left")

        # Génération du plan du cylindre
        self.cylindre = CylindreStirling(
            diametre_m=tech_sheet['Diametre_m'],
            course_m=tech_sheet['Course_m'],
            epaisseur_m=0.002,
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
        self.plan_path = "plan_cylindre.png"
        plot_cylindre(self.cylindre, self.plan_path)

        # Affichage du plan
        if os.path.exists(self.plan_path):
            image = Image.open(self.plan_path)
            image = image.resize((600, 300), Image.Resampling.LANCZOS)
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

        # Texte infos techniques
        c.setFont("Helvetica", 12)
        y = height - 90
        infos_text = [
            f"Diamètre interne (mm) : {self.tech_sheet['Diametre_m']*1000:.2f}",
            f"Course (mm) : {self.tech_sheet['Course_m']*1000:.2f}",
            f"Épaisseur (mm) : 2.00",
            f"Matière : Acier",
            f"Densité (kg/m³) : 7850",
            f"Rugosité (µm) : 0.8",
            f"État surface : Usinage fin",
            f"Température chaude (°C) : {self.tech_sheet['Temp_chaud_C']:.1f}",
            f"Température froide (°C) : {self.tech_sheet['Temp_froid_C']:.1f}",
            f"Nombre de vis : 6",
            f"Dimension vis ISO : M6",
            f"Entraxe vis (%) : 85",
            f"Limite rupture (MPa) : 700",
        ]
        for line in infos_text:
            c.drawString(30, y, line)
            y -= 20

        # Insérer l'image du plan
        if os.path.exists(self.plan_path):
            c.drawImage(self.plan_path, 30, y - 300, width=550, height=250, preserveAspectRatio=True)
            y -= 320

        c.save()
        print(f"PDF généré : {pdf_path}")

    def goto_back(self):
        from pages.parts_menu_page import PartsMenuPage
        self.master.show_page(PartsMenuPage, self.tech_sheet)
