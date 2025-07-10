# calculs/villebrequin.py

import math

class VillebrequinStirling:
    """
    Modélisation d’un vilebrequin de moteur Stirling pour CAO :
    - Dimensions maneton, bras, masses d’équilibrage, paliers
    - Masse, volume, matière, état de surface, moments d’inertie principaux
    """

    def __init__(
        self,
        nb_manetons=1,
        rayon_maneton_m=0.009,          # Rayon maneton (ex: 9mm, soit course totale = 18mm)
        largeur_maneton_m=0.010,        # Largeur maneton (ex: 10mm)
        diametre_axe_m=0.012,           # Diamètre de l’axe principal (ex: 12mm)
        longueur_axe_m=0.080,           # Longueur totale vilebrequin (ex: 80mm)
        largeur_bras_m=0.012,           # Largeur des bras (ex: 12mm)
        epaisseur_bras_m=0.010,         # Épaisseur des bras (ex: 10mm)
        diametre_contrepoids_m=0.028,   # Diamètre des masses d’équilibrage (ex: 28mm)
        largeur_contrepoids_m=0.010,    # Largeur masses d’équilibrage (ex: 10mm)
        matiere="Acier 18NiCrMo5",
        densite_kg_m3=7850,
        rugosite_um=1.6,
        etat_surface="Usinage + rectif",
    ):
        if nb_manetons < 1 or rayon_maneton_m <= 0 or largeur_maneton_m <= 0 or diametre_axe_m <= 0:
            raise ValueError("Paramètres invalides")
        self.nb_manetons = nb_manetons
        self.rayon_maneton = rayon_maneton_m
        self.largeur_maneton = largeur_maneton_m
        self.diametre_axe = diametre_axe_m
        self.longueur_axe = longueur_axe_m
        self.largeur_bras = largeur_bras_m
        self.epaisseur_bras = epaisseur_bras_m
        self.diametre_contrepoids = diametre_contrepoids_m
        self.largeur_contrepoids = largeur_contrepoids_m
        self.matiere = matiere
        self.densite = densite_kg_m3
        self.rugosite = rugosite_um
        self.etat_surface = etat_surface

    @property
    def volume_maneton(self):
        "Volume du/des maneton(s), cylindre(s) plein(s)"
        return self.nb_manetons * math.pi * (self.rayon_maneton ** 2) * self.largeur_maneton

    @property
    def volume_axe(self):
        "Volume de l’axe principal (hors bras et manetons)"
        return math.pi * (self.diametre_axe / 2) ** 2 * self.longueur_axe

    @property
    def volume_bras(self):
        "Volume des bras (rectangle simple, 2 bras par maneton)"
        return 2 * self.nb_manetons * self.largeur_bras * self.epaisseur_bras * self.rayon_maneton

    @property
    def volume_contrepoids(self):
        "Volume total des masses d’équilibrage"
        return 2 * self.nb_manetons * math.pi * (self.diametre_contrepoids / 2) ** 2 * self.largeur_contrepoids

    @property
    def volume_total(self):
        "Volume total estimé"
        return self.volume_axe + self.volume_maneton + self.volume_bras + self.volume_contrepoids

    @property
    def masse(self):
        "Masse totale (kg)"
        return self.volume_total * self.densite

    @property
    def surface_axe(self):
        "Surface latérale de l’axe (m²)"
        return math.pi * self.diametre_axe * self.longueur_axe

    @property
    def surface_manetons(self):
        "Surface latérale manetons (m²)"
        return self.nb_manetons * math.pi * 2 * self.rayon_maneton * self.largeur_maneton

    @property
    def surface_contrepoids(self):
        "Surface latérale masses d’équilibrage (m²)"
        return 2 * self.nb_manetons * math.pi * self.diametre_contrepoids * self.largeur_contrepoids

    @property
    def surface_totale(self):
        "Surface totale extérieure estimée (m²)"
        return self.surface_axe + self.surface_manetons + self.surface_contrepoids

    @property
    def moment_inertie_axe(self):
        "Moment d’inertie de l’axe principal (kg.m²) pour rotation centrale"
        m = self.densite * self.volume_axe
        R = self.diametre_axe / 2
        return 0.5 * m * R ** 2

    @property
    def moment_inertie_contrepoids(self):
        "Moment d’inertie masses d’équilibrage (par rapport à l’axe)"
        m = self.densite * self.volume_contrepoids
        R = self.diametre_contrepoids / 2
        return m * R ** 2 / 2

    def to_dict(self):
        return {
            "Nb manetons": self.nb_manetons,
            "Rayon maneton (mm)": round(self.rayon_maneton * 1000, 3),
            "Largeur maneton (mm)": round(self.largeur_maneton * 1000, 3),
            "Diamètre axe (mm)": round(self.diametre_axe * 1000, 3),
            "Longueur axe (mm)": round(self.longueur_axe * 1000, 3),
            "Largeur bras (mm)": round(self.largeur_bras * 1000, 3),
            "Épaisseur bras (mm)": round(self.epaisseur_bras * 1000, 3),
            "Diamètre contrepoids (mm)": round(self.diametre_contrepoids * 1000, 3),
            "Largeur contrepoids (mm)": round(self.largeur_contrepoids * 1000, 3),
            "Matière": self.matiere,
            "Densité (kg/m3)": self.densite,
            "Rugosité (Ra, µm)": self.rugosite,
            "État de surface": self.etat_surface,
            "Masse (kg)": round(self.masse, 5),
            "Volume total (cm3)": round(self.volume_total * 1e6, 3),
            "Surface totale (cm2)": round(self.surface_totale * 1e4, 3),
            "Moment inertie axe (g.mm2)": round(self.moment_inertie_axe * 1e7, 2),
            "Moment inertie contrepoids (g.mm2)": round(self.moment_inertie_contrepoids * 1e7, 2),
        }

    def __repr__(self):
        return (
            f"VillebrequinStirling({self.nb_manetons} manetons, "
            f"axe {self.diametre_axe*1000:.2f}x{self.longueur_axe*1000:.2f} mm, "
            f"maneton r={self.rayon_maneton*1000:.2f} mm, {self.largeur_maneton*1000:.2f} mm, "
            f"contrepoids {self.diametre_contrepoids*1000:.2f} mm, "
            f"{self.matiere}, Ra={self.rugosite} µm, {self.etat_surface})"
        )

# Exemple d’utilisation :
if __name__ == "__main__":
    vbrk = VillebrequinStirling(
        nb_manetons=1,
        rayon_maneton_m=0.009,
        largeur_maneton_m=0.010,
        diametre_axe_m=0.012,
        longueur_axe_m=0.080,
        largeur_bras_m=0.012,
        epaisseur_bras_m=0.010,
        diametre_contrepoids_m=0.028,
        largeur_contrepoids_m=0.010,
        matiere="Acier 18NiCrMo5",
        densite_kg_m3=7850,
        rugosite_um=1.6,
        etat_surface="Usinage + rectif"
    )
    print(vbrk)
    print("Paramètres CAO :", vbrk.to_dict())
