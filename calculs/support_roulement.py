# calculs\support_roulement.py

import math

# Tableau minimal de roulements à billes standard ISO (SKF 6000, 6001, ...)
ROULEMENTS_ISO = [
    {"ref": "6000", "d": 10.0, "D": 26.0, "B": 8.0, "charge_C": 4.55e3},
    {"ref": "6001", "d": 12.0, "D": 28.0, "B": 8.0, "charge_C": 5.10e3},
    {"ref": "6002", "d": 15.0, "D": 32.0, "B": 9.0, "charge_C": 6.55e3},
    {"ref": "6003", "d": 17.0, "D": 35.0, "B": 10.0, "charge_C": 7.90e3},
    {"ref": "6004", "d": 20.0, "D": 42.0, "B": 12.0, "charge_C": 9.65e3},
    # ... compléter au besoin
]

MATERIAUX_SUPP = {
    "Alu": {"densite": 2700, "limite": 140e6},
    "Acier": {"densite": 7850, "limite": 240e6},
    "Fonte": {"densite": 7200, "limite": 110e6},
}

# Tolerances ISO de logement (glissant H7, serrant N6...)
TOLERANCES_ISO = {
    "H7": 0.021,    # mm sur D jusqu'à 25 mm, voir ISO 286-2 pour détails
    "N6": 0.011,
}

def choix_roulement(d_arbre_mm, charge_radiale_N, type="billes"):
    """Sélectionne le premier roulement standard adapté en diamètre ET charge"""
    for roulement in ROULEMENTS_ISO:
        if roulement["d"] >= d_arbre_mm and roulement["charge_C"] >= charge_radiale_N:
            return roulement
    raise ValueError("Aucun roulement standard ISO trouvé pour cet arbre/charge.")

class SupportRoulement:
    """
    Modélisation d’un support de roulement pour CAO :
    - Géométrie, matière, masse, tolérances, RDM.
    - Choix auto du roulement standard
    """

    def __init__(
        self,
        d_arbre_mm,
        charge_radiale_N=1000,
        matiere="Alu",
        largeur_support_mm=20,
        epaisseur_mm=10,
        type_tolerance="H7",
        avec_circlips=False,
        avec_joint=False
    ):
        self.d_arbre_mm = d_arbre_mm
        self.charge_radiale_N = charge_radiale_N
        self.matiere = matiere
        self.largeur_support = largeur_support_mm
        self.epaisseur = epaisseur_mm
        self.type_tolerance = type_tolerance
        self.avec_circlips = avec_circlips
        self.avec_joint = avec_joint

        # Sélection du roulement
        self.roulement = choix_roulement(d_arbre_mm, charge_radiale_N)
        self.d_alésage = self.roulement["D"] + (TOLERANCES_ISO.get(type_tolerance, 0.021))
        self.largeur_roulement = self.roulement["B"]

    @property
    def masse(self):
        """Masse du support (approximé en cylindre plein hors alésage roulement)"""
        r_ext = (self.d_alésage / 2 + self.epaisseur)
        r_int = self.d_alésage / 2
        volume = math.pi * (r_ext**2 - r_int**2) * self.largeur_support / 1000  # mm3 -> cm3
        return volume * MATERIAUX_SUPP[self.matiere]["densite"] / 1e6  # en kg

    @property
    def contrainte_max(self):
        """Vérification RDM simple sous charge radiale (approchée)"""
        S = (self.d_alésage / 2) * self.largeur_support / 1000  # surface appui (mm2 -> cm2)
        if S <= 0: return 0
        return self.charge_radiale_N / (S * 1e-4)  # N / cm2 -> Pa

    def tol_alesage(self):
        """Tolérance d'alésage selon la norme"""
        return TOLERANCES_ISO.get(self.type_tolerance, 0.021)

    def to_dict(self):
        return {
            "Arbre (mm)": self.d_arbre_mm,
            "Charge radiale (N)": self.charge_radiale_N,
            "Matériau support": self.matiere,
            "Roulement choisi": self.roulement["ref"],
            "Alésage roulement (mm)": round(self.roulement["D"], 3),
            "Largeur roulement (mm)": round(self.roulement["B"], 3),
            "Tol. d'alésage (mm)": self.tol_alesage(),
            "Largeur support (mm)": self.largeur_support,
            "Épaisseur support (mm)": self.epaisseur,
            "Avec circlips": self.avec_circlips,
            "Avec joint": self.avec_joint,
            "Masse support (kg)": round(self.masse, 4),
            "Contrainte max (Pa)": int(self.contrainte_max),
        }

    def __repr__(self):
        return (
            f"SupportRoulement(Arbre={self.d_arbre_mm} mm, "
            f"Roulement={self.roulement['ref']}, "
            f"Alésage={self.roulement['D']:.2f} mm H7, "
            f"Charge={self.charge_radiale_N} N, Mat={self.matiere})"
        )

# EXEMPLE D'UTILISATION
if __name__ == "__main__":
    supp = SupportRoulement(
        d_arbre_mm=15,
        charge_radiale_N=4000,
        matiere="Acier",
        largeur_support_mm=22,
        epaisseur_mm=11,
        type_tolerance="H7",
        avec_circlips=True,
        avec_joint=True
    )
    print(supp)
    print("Paramètres CAO :", supp.to_dict())
