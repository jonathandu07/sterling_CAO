# pages\create_project_page.py
import tkinter as tk
from tkinter import ttk
from colors import *
from project_db import save_project, get_aes_key
import math

def auto_stirling_params(power_w):
    """Renvoie des valeurs typiques adaptées à la puissance demandée"""
    # Loi empirique adaptée, à moduler selon retour d’expérience
    if power_w < 300:
        Th = 500 + 0.001 * power_w    # 500 à 800K
        pm = 6 + (power_w / 100)      # 6 à 9 bar
        Nc = max(2, int(power_w // 100) + 1)
        f = 15 + (power_w / 30)       # 15 à 25 Hz
        eta = 30                      # %
    elif power_w < 3000:
        Th = 700 + (power_w-300)/2700*150   # ~700-850K
        pm = 10 + (power_w-300)/2700*8      # 10-18 bar
        Nc = 2 + int((power_w-300)/900)     # 2 à 4 cylindres
        f = 18 + (power_w-300)/2700*12      # 18-30 Hz
        eta = 35
    elif power_w < 15000:
        Th = 850 + (power_w-3000)/12000*100     # 850–950K
        pm = 18 + (power_w-3000)/12000*7        # 18-25 bar
        Nc = 4 + int((power_w-3000)/3000)       # 4 à 8
        f = 30 + (power_w-3000)/12000*15        # 30-45 Hz
        eta = 40
    else:
        Th = 950 + min(100, (power_w-15000)//15000*50)   # max 1050K
        pm = 25 + min(10, (power_w-15000)//15000*5)      # max 35 bar
        Nc = 8 + int((power_w-15000)//6000)
        f = 45
        eta = 45
    Tc = 300 # Ambiante
    return {
        "Th": round(Th, 2),
        "Tc": Tc,
        "eta": eta,
        "pm": round(pm, 2),
        "f": int(f),
        "Nc": Nc
    }



class CreateProjectPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG)
        self.master = master
        self.tech_sheet = None
        self.validated = False
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.create_ui()

    def create_ui(self):
        # --- Frame centrale ---
        main_frame = tk.Frame(self, bg=GW)
        main_frame.grid(row=0, column=0, padx=40, pady=30, sticky="nsew")
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(12, weight=1)

        # --- Titre ---
        tk.Label(main_frame, text="Créer un projet : Cahier des Charges",
                 font=("Segoe UI", 17, "bold"), fg=BF, bg=GW
                 ).grid(row=0, column=0, columnspan=2, pady=(0, 18), sticky="w")

        # --- Entrées utilisateur ---
        self.inputs = {}
        fields = [
            ("Nom du projet *", "name"),
            ("Puissance cible (W) *", "P"),
            ("Temp. chaude (K) *", "Th"),
            ("Temp. froide (K) *", "Tc"),
            ("Rendement (%) *", "eta"),
            ("Pression gaz (bar) *", "pm"),
            ("Fréquence (Hz) *", "f"),
            ("Nombre de cylindres *", "Nc"),
            ("Course (mm, option)", "C"),
        ]

        for i, (label, key) in enumerate(fields):
            tk.Label(main_frame, text=label, font=("Segoe UI", 12), bg=GW, fg=BF
                     ).grid(row=i+1, column=0, sticky="e", pady=5, padx=3)
            entry = tk.Entry(main_frame, font=("Segoe UI", 12))
            entry.grid(row=i+1, column=1, sticky="ew", pady=5, padx=3)
            self.inputs[key] = entry

        # Gaz de travail (combobox)
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

        # --- Résumé technique (scrollable) ---
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

        # --- Bas : boutons et champ mot de passe ---
        bottom_frame = tk.Frame(main_frame, bg=GW)
        bottom_frame.grid(row=12, column=0, columnspan=2, sticky="ew", pady=(15, 5))
        bottom_frame.grid_columnconfigure(0, weight=1)
        bottom_frame.grid_columnconfigure(1, weight=1)
        bottom_frame.grid_columnconfigure(2, weight=1)
        bottom_frame.grid_columnconfigure(3, weight=1)

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

        # Rendre la fenêtre principale redimensionnable !
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

        # Puissance (obligatoire)
        try:
            P = float(self.inputs["P"].get().strip())
            if P <= 0: raise Exception()
        except Exception:
            self.update_summary("Tu dois saisir la puissance cible (en W).", color=RV)
            self.tech_sheet = None
            self.btn_validate.config(state="disabled")
            return

        # Auto-calcule des valeurs typiques selon la puissance (modèle évolutif)
        default_values = auto_stirling_params(P)

        # Pour chaque champ, si vide, on injecte la valeur calculée
        params = {}
        for key in ["Th", "Tc", "eta", "pm", "f", "Nc"]:
            val = self.inputs[key].get().strip()
            if not val:
                self.inputs[key].delete(0, tk.END)
                self.inputs[key].insert(0, str(default_values[key]))
                params[key] = default_values[key]
            else:
                params[key] = float(val) if key != "Nc" else int(val)

        eta = params["eta"] / 100
        pm = params["pm"] * 1e5
        f = params["f"]
        Nc = int(params["Nc"])
        Th = params["Th"]
        Tc = params["Tc"]

        # Course (optionnelle)
        try:
            c_val = self.inputs["C"].get().strip()
            C = float(c_val) / 1000 if c_val else None
        except:
            C = None

        gaz = self.gaz_var.get() or "Air"
        dT = (Th - Tc) / Th
        Vs = P / (Nc * pm * f * dT * eta)
        # Calcul du diamètre si course connue
        D = None
        if C:
            D = math.sqrt(4 * Vs / (math.pi * C))

        # Architecture dynamique selon le nombre de cylindres
        archi = "En ligne"
        if Nc == 2:
            archi = "À plat (Boxer) ou en ligne"
        elif 3 <= Nc <= 4:
            archi = "En ligne ou en V"
        elif 5 <= Nc <= 6:
            archi = "V ou Étoile"
        elif 7 <= Nc <= 9:
            archi = "Étoile"
        elif Nc >= 10:
            archi = "Double étoile ou W"

        resume = f"Cahier des charges technique généré :\n"
        resume += f" - Volume balayé/cyl : {Vs*1e6:.2f} cm³\n"
        if D:
            resume += f" - Diamètre cyl. : {D*100:.2f} mm\n"
            resume += f" - Course : {C*1000:.2f} mm\n"
        else:
            resume += f" - Course à saisir pour calculer le diamètre\n"
        resume += f" - Nb cylindres : {Nc}\n"
        resume += f" - Gaz de travail : {gaz}\n"
        resume += f" - Architecture suggérée : {archi}\n"
        self.update_summary(resume, color=VO)
        self.tech_sheet = {
            "Volume_balaye_m3": Vs,
            "Diametre_m": D,
            "Course_m": C,
            "Nb_cylindres": Nc,
            "Gaz_de_travail": gaz,
            "Architecture": archi,
            "Parametres_fonctionnels": {
                "Puissance": P, "T_chaude": Th, "T_froide": Tc,
                "Rendement": eta, "Pression": pm, "Frequence": f,
            }
        }
        self.btn_validate.config(state="normal")
        self.btn_edit.config(state="disabled")
        self.btn_continue.config(state="disabled")
        self.btn_save.config(state="disabled")
        self.validated = False

    def validate_tech_sheet(self):
        if not self.tech_sheet:
            self.update_summary("Génère d’abord le cahier technique.", color=RV)
            return
        # Lock inputs
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
        print("Redirection vers le listing des pièces nécessaires…")
        # self.master.show_page(PartsListPage, self.tech_sheet)
