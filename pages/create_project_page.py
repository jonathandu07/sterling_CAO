# pages/create_project_page.py
import tkinter as tk
from tkinter import ttk
from colors import *
from project_db import save_project, get_aes_key

from calculs.stirling import calcul_complet
from calculs.cylindre import CylindreStirling
from calculs.piston import PistonStirling
from calculs.bielle import BielleStirling
from pages.parts_menu_page import PartsMenuPage

class CreateProjectPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG)
        self.master = master
        self.tech_sheet = None
        self.parts_resume = None
        self.validated = False
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.create_ui()

    def create_ui(self):
        main_frame = tk.Frame(self, bg=GW)
        main_frame.grid(row=0, column=0, padx=40, pady=30, sticky="nsew")
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(10, weight=1)

        tk.Label(main_frame, text="Créer un projet : Cahier des Charges",
                 font=("Segoe UI", 17, "bold"), fg=BF, bg=GW
                 ).grid(row=0, column=0, columnspan=2, pady=(0, 18), sticky="w")

        self.inputs = {}

        fields = [
            ("Nom du projet *", "name"),
            ("Puissance cible (W) *", "P"),
        ]
        for i, (label, key) in enumerate(fields):
            tk.Label(main_frame, text=label, font=("Segoe UI", 12), bg=GW, fg=BF
                     ).grid(row=i+1, column=0, sticky="e", pady=5, padx=3)
            entry = tk.Entry(main_frame, font=("Segoe UI", 12))
            entry.grid(row=i+1, column=1, sticky="ew", pady=5, padx=3)
            self.inputs[key] = entry

        # Architecture affichée, mais grisée/non éditable
        tk.Label(main_frame, text="Architecture", font=("Segoe UI", 12), bg=GW, fg=BF
                 ).grid(row=3, column=0, sticky="e", pady=5, padx=3)
        self.arch_var = tk.StringVar(value="En ligne")
        self.arch_combobox = ttk.Combobox(main_frame, textvariable=self.arch_var,
                                          values=[
                                              "En ligne", "En V", "À plat (Boxer)",
                                              "Étoile", "W", "Double étoile"
                                          ], font=("Segoe UI", 11), state="disabled")
        self.arch_combobox.grid(row=3, column=1, sticky="ew", pady=5, padx=3)

        # Gaz de travail
        tk.Label(main_frame, text="Gaz de travail", font=("Segoe UI", 12), bg=GW, fg=BF
                 ).grid(row=4, column=0, sticky="e", pady=5, padx=3)
        self.gaz_var = tk.StringVar(value="Air")
        self.gaz_combobox = ttk.Combobox(main_frame, textvariable=self.gaz_var,
                                         values=[
                                             "Air", "Gaz d'échappement (cycle régénératif)",
                                             "Hélium (He)", "Hydrogène (H₂)", "Azote (N₂)", "Dioxyde de carbone (CO₂)",
                                         ], font=("Segoe UI", 11), state="readonly")
        self.gaz_combobox.grid(row=4, column=1, sticky="ew", pady=5, padx=3)

        # Résumé technique (scrollable)
        summary_frame = tk.Frame(main_frame, bg=GW)
        summary_frame.grid(row=6, column=0, columnspan=2, sticky="nsew", pady=(16, 0))
        summary_frame.grid_rowconfigure(0, weight=1)
        summary_frame.grid_columnconfigure(0, weight=1)
        summary_scrollbar = tk.Scrollbar(summary_frame)
        summary_scrollbar.pack(side="right", fill="y")
        self.tech_label = tk.Text(
            summary_frame, height=8, width=65,
            font=("Consolas", 10), bg=GW, fg=VG, wrap="word",
            yscrollcommand=summary_scrollbar.set, borderwidth=1, relief="solid")
        self.tech_label.pack(fill="both", expand=True)
        self.tech_label.config(state="disabled")
        summary_scrollbar.config(command=self.tech_label.yview)

        # Bas : boutons
        bottom_frame = tk.Frame(main_frame, bg=GW)
        bottom_frame.grid(row=8, column=0, columnspan=2, sticky="ew", pady=(15, 5))
        for i in range(4): bottom_frame.grid_columnconfigure(i, weight=1)

        self.btn_calc = tk.Button(bottom_frame, text="Calculer le cahier technique",
                                  bg=JV, fg=GW, font=("Segoe UI", 11, "bold"),
                                  relief="flat", command=self.generate_tech_sheet, cursor="hand2")
        self.btn_calc.grid(row=0, column=0, padx=3, ipadx=6)
        self.btn_validate = tk.Button(bottom_frame, text="Valider", bg=BA, fg=GW, font=("Segoe UI", 10, "bold"),
                                      relief="flat", command=self.validate_tech_sheet, cursor="hand2", state="disabled")
        self.btn_validate.grid(row=0, column=1, padx=3, ipadx=6)
        self.btn_edit = tk.Button(bottom_frame, text="Modifier", bg=VO, fg=GW, font=("Segoe UI", 10, "bold"),
                                 relief="flat", command=self.edit_tech_sheet, cursor="hand2", state="disabled")
        self.btn_edit.grid(row=0, column=2, padx=3, ipadx=6)
        self.btn_continue = tk.Button(bottom_frame, text="Continuer", bg=BA, fg=GW, font=("Segoe UI", 10, "bold"),
                                      relief="flat", command=self.continue_to_parts, cursor="hand2", state="disabled")
        self.btn_continue.grid(row=0, column=3, padx=3, ipadx=6)

    def update_summary(self, text, color=VG):
        self.tech_label.config(state="normal")
        self.tech_label.delete("1.0", tk.END)
        self.tech_label.insert(tk.END, text)
        self.tech_label.tag_configure("color", foreground=color)
        self.tech_label.config(state="disabled")

    def generate_tech_sheet(self):
        name = self.inputs["name"].get().strip()
        if not name:
            self.update_summary("Tu dois donner un nom au projet.", color=RV)
            self.tech_sheet = None
            self.btn_validate.config(state="disabled")
            return

        try:
            P = float(self.inputs["P"].get().strip())
            if P <= 0:
                raise Exception()
        except Exception:
            self.update_summary("Puissance cible invalide (en W).", color=RV)
            self.tech_sheet = None
            self.btn_validate.config(state="disabled")
            return

        gaz = self.gaz_var.get() or "Air"

        try:
            tech = calcul_complet(
                P=P,
                gaz=gaz
            )
            Nc = tech["Nb_cylindres"]
            archi = tech["Architecture"]
            # Affiche l'archi proposée, n’active jamais l'édition utilisateur
            self.arch_var.set(archi)

            resume = f"Cahier technique généré :\n"
            resume += f" - Puissance cible : {P:.2f} W\n"
            resume += f" - Nombre de cylindres : {Nc}\n"
            resume += f" - Architecture suggérée : {archi}\n"
            resume += f" - Gaz : {gaz}\n"
            resume += f" - Temp. chaude : {tech['Temp_chaud_C']:.1f} °C\n"
            resume += f" - Temp. froide : {tech['Temp_froid_C']:.1f} °C\n"
            resume += f" - Diamètre cylindre : {tech['Diametre_interne_m']*1000:.2f} mm\n"
            resume += f" - Course : {tech['Course_m']*1000:.2f} mm\n"
            self.update_summary(resume, color=VO)

            self.tech_sheet = tech
            self.btn_validate.config(state="normal")
            self.btn_edit.config(state="disabled")
            self.btn_continue.config(state="disabled")
            self.validated = False
            self.parts_resume = None

        except Exception as e:
            self.update_summary(f"Erreur de calcul : {str(e)}", color=RV)
            self.tech_sheet = None
            self.btn_validate.config(state="disabled")
            return

    def validate_tech_sheet(self):
        if not self.tech_sheet:
            self.update_summary("Génère d’abord le cahier technique.", color=RV)
            return
        for entry in self.inputs.values():
            entry.config(state="readonly")
        self.gaz_combobox.config(state="disabled")
        self.arch_combobox.config(state="disabled")
        self.btn_validate.config(state="disabled")
        self.btn_edit.config(state="normal")
        self.btn_continue.config(state="normal")
        self.update_summary("Cahier technique validé. Tu peux continuer.\n\n"
                            + self.tech_label.get("1.0", tk.END), color=JV)
        self.validated = True

        # 👉 Ajoute cette ligne :
        self.master.show_page(PartsMenuPage, self.tech_sheet)


    def edit_tech_sheet(self):
        for entry in self.inputs.values():
            entry.config(state="normal")
        self.gaz_combobox.config(state="readonly")
        self.arch_combobox.config(state="disabled")
        self.btn_validate.config(state="normal")
        self.btn_edit.config(state="disabled")
        self.btn_continue.config(state="disabled")
        self.update_summary("Modifie puis régénère le cahier technique.", color=VO)
        self.validated = False

    def continue_to_parts(self):
        if not self.validated:
            self.update_summary("Valide d'abord le cahier technique.", color=RV)
            return
        self.generate_parts_summary()

    def generate_parts_summary(self):
        tech = self.tech_sheet
        try:
            cyl = CylindreStirling(
                diametre_m=tech["Diametre_interne_m"],
                course_m=tech["Course_m"],
                epaisseur_m=0.003,
                matiere=tech["Materiau"] if "Materiau" in tech else "Acier",
                densite_kg_m3=7850,
                rugosite_um=0.8,
                etat_surface="Usinage fin",
                Th=tech["Temp_chaud_C"]+273.15,
                Tc=tech["Temp_froid_C"]+273.15,
                nb_vis=6,
                dim_vis_iso="M6",
                entraxe_vis_pct=0.85,
                limite_rupture_MPa=700
            )
            piston = PistonStirling(
                diametre_m=tech["Diametre_interne_m"]-0.0002,
                hauteur_m=tech["Course_m"]*0.95,
                epaisseur_fond_m=0.003,
                epaisseur_jupe_m=0.002,
                hauteur_jupe_m=tech["Course_m"]*0.85,
                matiere="AlSi12",
                densite_kg_m3=2680,
                rugosite_um=0.6,
                etat_surface="Microbillage + rectif",
                nb_rainures=2,
                axe_diam_m=0.008,
                axe_longueur_m=tech["Diametre_interne_m"]*1.1
            )
            bielle = BielleStirling(
                longueur_m=tech["Course_m"]*2.6,
                largeur_corps_m=0.012,
                epaisseur_corps_m=0.004,
                diametre_tete_m=0.018,
                diametre_pied_m=0.010,
                axe_tete_diam_m=0.008,
                axe_pied_diam_m=0.008,
                matiere="Acier 42CrMo4",
                densite_kg_m3=7850,
                etat_surface="Usinage + rectif",
                rugosite_um=0.8
            )

            resume = f"=== Résumé des pièces principales ===\n"
            resume += f"[Cylindre]\n{cyl}\n{cyl.to_dict()}\n\n"
            resume += f"[Piston]\n{piston}\n{piston.to_dict()}\n\n"
            resume += f"[Bielle]\n{bielle}\n{bielle.to_dict()}\n\n"
            self.update_summary(resume, color=JV)
            self.parts_resume = resume

        except Exception as e:
            self.update_summary(f"Erreur lors du calcul des pièces : {e}", color=RV)
            self.parts_resume = None
