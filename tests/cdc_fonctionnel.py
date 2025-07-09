import tkinter as tk
from tkinter import ttk, messagebox
import math

class CDCFonctionnelApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cahier des Charges Fonctionnel - Moteur Stirling Nouvelle Génération")
        self.configure(bg="#f8fafc")
        self.geometry("640x800")

        self.font = ("Segoe UI", 11)
        self.create_widgets()

    def create_widgets(self):
        titre = tk.Label(self, text="🛠️ Cahier des Charges Fonctionnel", font=("Segoe UI", 20, "bold"), bg="#f8fafc", fg="#1e293b")
        titre.pack(pady=16)

        frm = tk.Frame(self, bg="#f8fafc")
        frm.pack(fill="both", expand=True, padx=20)

        # Champs d'entrée texte
        self.entrees = {}
        champs = [
            ("Puissance visée (W)", "Ex: 2000"),
            ("Couple attendu (Nm)", "Ex: 15"),
            ("Encombrement maximal (L x l x h, mm)", "Ex: 600 x 400 x 300"),
            ("Durée de fonctionnement souhaitée (heures)", "Ex: 10000"),
            ("Niveau sonore max (dB)", "Ex: 65"),
            ("Contraintes d’environnement (T°, humidité, altitude…)", "Ex: -20 à 45°C, 80% HR, 2000m"),
            ("Maintenance (simple, expert, auto…)", "Ex: simple"),
            ("Budget max (€)", "Ex: 5000"),
            ("Autres contraintes/exigences", "Ex: IP65, poids < 40kg"),
        ]

        for i, (label, ph) in enumerate(champs):
            lbl = tk.Label(frm, text=label, font=self.font, bg="#f8fafc", anchor="w")
            lbl.grid(row=i, column=0, sticky="w", pady=6)
            entry = ttk.Entry(frm, font=self.font)
            entry.grid(row=i, column=1, pady=6, sticky="ew")
            entry.insert(0, "")
            entry.config(width=32)
            self.entrees[label] = entry

        frm.grid_columnconfigure(1, weight=1)

        # Carburants (sélection multiple)
        lbl_carburant = tk.Label(frm, text="Carburant(s) utilisable(s)", font=self.font, bg="#f8fafc", anchor="w")
        lbl_carburant.grid(row=len(champs), column=0, sticky="w", pady=(12, 2))
        carburants = [
            "Hydrogène", "Méthane (gaz naturel)", "Propane", "Butane", "GPL", "Essence", "Gazole",
            "Bioéthanol", "Kérosène", "Alcool (méthanol/éthanol)", "Huile végétale", "Bois (gazéification)",
            "Charbon (gazéification)", "Solaire (miroirs)", "Électricité (résistance)", "Air comprimé"
        ]
        self.carburant_vars = {}
        carburant_frame = tk.Frame(frm, bg="#f8fafc")
        carburant_frame.grid(row=len(champs), column=1, sticky="w", pady=(12, 2))
        for i, c in enumerate(carburants):
            var = tk.BooleanVar()
            chk = ttk.Checkbutton(carburant_frame, text=c, variable=var)
            chk.grid(row=i // 2, column=i % 2, sticky="w", padx=5, pady=2)
            self.carburant_vars[c] = var

        # Option moteur à air comprimé/récupération gaz
        self.air_comprime_var = tk.BooleanVar()
        chk_air = ttk.Checkbutton(frm, text="Possibilité de recycler les gaz d'échappement et fonctionner à l'air comprimé (mode hybride)", variable=self.air_comprime_var)
        chk_air.grid(row=len(champs)+len(carburants)//2+2, column=0, columnspan=2, sticky="w", pady=(14,6))

        # Bouton de validation
        btn = ttk.Button(self, text="Valider et afficher le cahier des charges technique", command=self.generer_cdc_technique)
        btn.pack(pady=22)

    def generer_cdc_technique(self):
        # Récupère les données
        cdc = {k: v.get() for k, v in self.entrees.items()}
        cdc["Carburants"] = [c for c, var in self.carburant_vars.items() if var.get()]
        cdc["Air comprimé/récupération gaz"] = bool(self.air_comprime_var.get())

        # Traitement intelligent des valeurs numériques
        try:
            puissance = float(cdc.get("Puissance visée (W)", "0") or 0)
        except Exception:
            puissance = 0
        try:
            couple = float(cdc.get("Couple attendu (Nm)", "0") or 0)
        except Exception:
            couple = 0
        mode_hybride = cdc.get("Air comprimé/récupération gaz", False)
        carburants = cdc.get("Carburants", [])

        # Calcul technique automatique
        if puissance < 1000:
            nb_cylindres = 1
        elif puissance < 3000:
            nb_cylindres = 2
        else:
            nb_cylindres = 4

        pression_moy = 1_000_000  # 10 bars en Pascal
        rendement = 0.35
        frequence = 10
        course = 0.06   # 60 mm
        try:
            surface_piston = puissance / (pression_moy * course * frequence * nb_cylindres * rendement)
            diametre_piston = math.sqrt(surface_piston * 4 / math.pi)
        except ZeroDivisionError:
            surface_piston = 0
            diametre_piston = 0

        # Construction du CDC technique
        cdc_tech = {
            "Nombre de cylindres": nb_cylindres,
            "Course du piston (mm)": round(course * 1000, 1),
            "Diamètre du/de(s) piston(s) (mm)": round(diametre_piston * 1000, 1),
            "Pression moyenne de fonctionnement (bar)": pression_moy / 1e5,
            "Fréquence de fonctionnement (Hz)": frequence,
            "Rendement mécanique visé": rendement,
            "Architecture carburant": ", ".join(carburants),
            "Mode hybride air comprimé": "Oui" if mode_hybride else "Non",
            "Isolation acoustique": cdc.get("Niveau sonore max (dB)", "À définir"),
            "Refroidissement": "Liquide" if puissance > 2000 else "Air",
            "Matériaux recommandés": "Tête chaude Inconel/acier réfractaire, corps alu/inox",
            "Type de brûleur": "Modulaire, multicarburant",
            "Notes": "Prévoir circuit de recyclage gaz pour fonctionnement air comprimé" if mode_hybride else ""
        }

        # Affichage du CDC technique
        resume = "==== Cahier des Charges Technique ====\n"
        for cle, val in cdc_tech.items():
            resume += f"- {cle} : {val}\n"

        messagebox.showinfo("Cahier des charges technique généré", resume)

if __name__ == "__main__":
    app = CDCFonctionnelApp()
    app.mainloop()
