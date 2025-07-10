# pages/create_project_page.py

import tkinter as tk
from tkinter import ttk
from colors import *
from project_db import save_project, get_aes_key

# Importe tous les modules de calculs nécessaires
from calculs.stirling import calcul_complet
from calculs.cylindre import CylindreStirling
from calculs.piston import PistonStirling
from calculs.bielle import BielleStirling
from calculs.visserie import calc_visserie
from calculs.joints import calc_joints
from calculs.support_roulement import SupportRoulement

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
        main_frame.grid_rowconfigure(12, weight=1)

        tk.Label(main_frame, text="Créer un projet : Cahier des Charges",
                 font=("Segoe UI", 17, "bold"), fg=BF, bg=GW
                 ).grid(row=0, column=0, columnspan=2, pady=(0, 18), sticky="w")

        self.inputs = {}
        fields = [
            ("Nom du projet *", "name"),
            ("Puissance cible (W) *", "P"),
            ("Temp. chaude (K)", "Th"),
            ("Temp. froide (K)", "Tc"),
            ("Rendement (%)", "eta"),
            ("Pression gaz (bar)", "pm"),
            ("Fréquence (Hz)", "f"),
            ("Nombre de cylindres *", "Nc"),
            ("Course (mm, option)", "C"),
        ]

        for i, (label, key) in enumerate(fields):
            tk.Label(main_frame, text=label, font=("Segoe UI", 12), bg=GW, fg=BF
                     ).grid(row=i+1, column=0, sticky="e", pady=5, padx=3)
            entry = tk.Entry(main_frame, font=("Segoe UI", 12))
            entry.grid(row=i+1, column=1, sticky="ew", pady=5, padx=3)
            self.inputs[key] = entry

        tk.Label(main_frame, text="Gaz de travail", font=("Segoe UI", 12), bg=GW, fg=BF
                 ).grid(row=10, column=0, sticky="e", pady=5, padx=3)
        self.gaz_options = [
            "Air",
            "Gaz d'échappement (cycle régénératif)",
            "Hélium (He)",
            "Hydrogène (H₂)",
            "Azote (N₂)",
            "Dioxyde de carbone (CO₂)",
        ]
        self.gaz_var = tk.StringVar(value="Air")
        self.gaz_combobox = ttk.Combobox(main_frame, textvariable=self.gaz_var,
                                         values=self.gaz_options, font=("Segoe UI", 11),
                                         state="readonly")
        self.gaz_combobox.grid(row=10, column=1, sticky="ew", pady=5, padx=3)

        # Résumé technique (scrollable)
        summary_frame = tk.Frame(main_frame, bg=GW)
        summary_frame.grid(row=11, column=0, columnspan=2, sticky="nsew", pady=(16, 0))
        summary_frame.grid_rowconfigure(0, weight=1)
        summary_frame.grid_columnconfigure(0, weight=1)
        summary_scrollbar = tk.Scrollbar(summary_frame)
        summary_scrollbar.pack(side="right", fill="y")
        self.tech_label = tk.Text(
            summary_frame, height=5, width=60,
            font=("Consolas", 10), bg=GW, fg=VG, wrap="word",
            yscrollcommand=summary_scrollbar.set, borderwidth=1, relief="solid")
        self.tech_label.pack(fill="both", expand=True)
        self.tech_label.config(state="disabled")
        summary_scrollbar.config(command=self.tech_label.yview)

        # Bas : boutons et champ mot de passe
        bottom_frame = tk.Frame(main_frame, bg=GW)
        bottom_frame.grid(row=12, column=0, columnspan=2, sticky="ew", pady=(15, 5))
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

        pw_frame = tk.Frame(main_frame, bg=GW)
        pw_frame.grid(row=13, column=0, columnspan=2, sticky="ew", pady=(8, 5))
        tk.Label(pw_frame, text="Mot de passe AES :", font=("Segoe UI", 10), bg=GW, fg=VG
                 ).pack(side="left")
        self.password_entry = tk.Entry(pw_frame, show="*", width=18, font=("Segoe UI", 11))
        self.password_entry.pack(side="left", padx=8)
        self.btn_save = tk.Button(pw_frame, text="Sauvegarder", bg=JV, fg=GW, font=("Segoe UI", 10, "bold"),
                                  relief="flat", command=self.save_project, cursor="hand2", state="disabled")
        self.btn_save.pack(side="left", padx=8)

        self.master.resizable(True, True)
        self.master.minsize(820, 680)

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

        # Récupère la puissance (obligatoire)
        try:
            P = float(self.inputs["P"].get().strip())
            if P <= 0: raise Exception()
        except Exception:
            self.update_summary("Tu dois saisir la puissance cible (en W).", color=RV)
            self.tech_sheet = None
            self.btn_validate.config(state="disabled")
            return

        # Récupère ou laisse vide les champs personnalisés (ils seront surchargés si vides)
        champs = ["Th", "Tc", "eta", "pm", "f", "Nc", "C"]
        params = {}
        for key in champs:
            val = self.inputs[key].get().strip()
            params[key] = float(val) if val else None
        params["Nc"] = int(params["Nc"]) if params["Nc"] is not None else None
        gaz = self.gaz_var.get() or "Air"

        # Calcul complet via le module calculs.stirling
        tech = calcul_complet(
            P=P,
            Th=params["Th"],
            Tc=params["Tc"],
            pm=params["pm"]*1e5 if params["pm"] else None,  # Conversion bar → Pa
            f=params["f"],
            Nc=params["Nc"],
            eta=params["eta"],
            C=params["C"]/1000 if params["C"] else None,    # mm → m
            gaz=gaz
        )

        resume = f"Cahier des charges technique généré :\n"
        resume += f" - Volume balayé/cyl : {tech['Volume_balayé_m3']*1e6:.2f} cm³\n"
        resume += f" - Diamètre cyl. : {tech['Diametre_m']*100:.2f} mm\n"
        resume += f" - Course : {tech['Course_m']*1000:.2f} mm\n"
        resume += f" - Nb cylindres : {tech['Nb_cylindres']}\n"
        resume += f" - Gaz de travail : {tech['Gaz']}\n"
        resume += f" - Architecture suggérée : {tech['Architecture']}\n"
        self.update_summary(resume, color=VO)

        self.tech_sheet = tech
        self.btn_validate.config(state="normal")
        self.btn_edit.config(state="disabled")
        self.btn_continue.config(state="disabled")
        self.btn_save.config(state="disabled")
        self.validated = False
        self.parts_resume = None

    def validate_tech_sheet(self):
        if not self.tech_sheet:
            self.update_summary("Génère d’abord le cahier technique.", color=RV)
            return
        for entry in self.inputs.values():
            entry.config(state="readonly")
        self.gaz_combobox.config(state="disabled")
        self.btn_validate.config(state="disabled")
        self.btn_edit.config(state="normal")
        self.btn_continue.config(state="normal")
        self.btn_save.config(state="normal")
        self.update_summary("Cahier technique validé. Tu peux continuer ou sauvegarder.\n\n"
                            + self.tech_label.get("1.0", tk.END), color=JV)
        self.validated = True

    def edit_tech_sheet(self):
        for entry in self.inputs.values():
            entry.config(state="normal")
        self.gaz_combobox.config(state="readonly")
        self.btn_validate.config(state="normal")
        self.btn_edit.config(state="disabled")
        self.btn_continue.config(state="disabled")
        self.btn_save.config(state="disabled")
        self.update_summary("Modifie puis régénère le cahier technique.", color=VO)
        self.validated = False

    def save_project(self):
        if not self.validated:
            self.update_summary("Valide d'abord le cahier technique.", color=RV)
            return
        name = self.inputs["name"].get()
        password = self.password_entry.get()
        if not name or not password:
            self.update_summary("Nom de projet et mot de passe obligatoires.", color=RV)
            return
        aes_key = get_aes_key(password)
        save_project(name, self.tech_sheet, aes_key)
        self.update_summary("Projet sauvegardé avec succès !", color=JV)

    def continue_to_parts(self):
        if not self.validated:
            self.update_summary("Valide d'abord le cahier technique.", color=RV)
            return
        self.generate_parts_summary()

    def generate_parts_summary(self):
        """Génère le résumé technique complet des pièces à partir du cahier technique validé."""
        tech = self.tech_sheet
        try:
            cyl = CylindreStirling(
                diametre_m=tech["Diametre_m"],
                course_m=tech["Course_m"],
                epaisseur_m=0.002,  # à personnaliser selon projet
                matiere="Acier",
                densite_kg_m3=7850,
                rugosite_um=0.8,
                etat_surface="Usinage fin",
                Th=tech["Temp_chaud_K"],
                Tc=tech["Temp_froid_K"],
                nb_vis=6,
                dim_vis_iso="M6",
                entraxe_vis_pct=0.85,
                limite_rupture_MPa=700
            )
            piston = PistonStirling(
                diametre_m=tech["Diametre_m"]-0.0002,
                hauteur_m=tech["Course_m"]*0.95,
                epaisseur_fond_m=0.003,
                epaisseur_jupe_m=0.002,
                matiere="AlSi12",
                densite_kg_m3=2680,
                rugosite_um=0.6,
                etat_surface="Microbillage + rectif",
                nb_rainures=2,
                axe_diam_m=0.008,
                axe_longueur_m=tech["Diametre_m"]*1.1
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
            vis = calc_visserie(
                cyl.nb_vis, cyl.dim_vis_iso, cyl.diam_percage_vis, cyl.epaisseur, cyl.entraxe_vis
            )
            joints = calc_joints(
                diametre_arbre=tech["Diametre_m"],
                profondeur=0.002,
                pression=tech["Pression_Pa"] if "Pression_Pa" in tech else 100000
            )
            roulement = SupportRoulement(
                d_arbre_mm=8, charge_radiale_N=2000, matiere="Acier"
            )

            resume = f"=== Résumé des pièces principales ===\n"
            resume += f"[Cylindre]\n{cyl}\n{cyl.to_dict()}\n\n"
            resume += f"[Piston]\n{piston}\n{piston.to_dict()}\n\n"
            resume += f"[Bielle]\n{bielle}\n{bielle.to_dict()}\n\n"
            resume += f"[Visserie]\n{vis}\n\n"
            resume += f"[Joints toriques]\n{joints}\n\n"
            resume += f"[Roulement]\n{roulement}\n{roulement.to_dict()}\n\n"

            self.update_summary(resume, color=JV)
            self.parts_resume = resume
        except Exception as e:
            self.update_summary(f"Erreur lors du calcul des pièces : {e}", color=RV)
            self.parts_resume = None
