# calculs/bielle.py

import math

class BielleStirling:
    """
    Modélisation d’une bielle de moteur Stirling pour CAO :
    - Géométrie complète (longueur, diamètres axes)
    - Masse, matière, état de surface, résistance, volume, etc.
    - Calculs adaptés pour bielle usinée (rectangulaire ou en I)
    """

    def __init__(
        self,
        longueur_m,
        largeur_corps_m=0.012,            # Largeur de la bielle (ex : 12 mm)
        epaisseur_corps_m=0.004,          # Épaisseur du corps (ex : 4 mm)
        diametre_tete_m=0.018,            # Diamètre tête bielle côté maneton (ex : 18 mm)
        diametre_pied_m=0.010,            # Diamètre pied côté piston (ex : 10 mm)
        axe_tete_diam_m=0.008,            # Axe tête (ex : 8 mm)
        axe_pied_diam_m=0.008,            # Axe pied (ex : 8 mm)
        matiere="Acier 42CrMo4",
        densite_kg_m3=7850,
        etat_surface="Usinage standard",
        rugosite_um=1.2
    ):
        if longueur_m <= 0 or largeur_corps_m <= 0 or epaisseur_corps_m <= 0:
            raise ValueError("Dimensions invalides")
        self.longueur = longueur_m
        self.largeur = largeur_corps_m
        self.epaisseur = epaisseur_corps_m
        self.diametre_tete = diametre_tete_m
        self.diametre_pied = diametre_pied_m
        self.axe_tete_diam = axe_tete_diam_m
        self.axe_pied_diam = axe_pied_diam_m
        self.matiere = matiere
        self.densite = densite_kg_m3
        self.etat_surface = etat_surface
        self.rugosite = rugosite_um

    @property
    def section(self):
        "Section droite de la bielle (m²) (rectangulaire par défaut)"
        return self.largeur * self.epaisseur

    @property
    def volume_corps(self):
        "Volume du corps de bielle (m³)"
        return self.section * self.longueur

    @property
    def volume_tete(self):
        "Volume tête (approximé en cylindre plein, m³)"
        return math.pi * (self.diametre_tete / 2) ** 2 * self.epaisseur

    @property
    def volume_pied(self):
        "Volume pied (approximé en cylindre plein, m³)"
        return math.pi * (self.diametre_pied / 2) ** 2 * self.epaisseur

    @property
    def volume_total(self):
        "Volume total de la bielle (m³)"
        return self.volume_corps + self.volume_tete + self.volume_pied

    @property
    def masse(self):
        "Masse totale (kg)"
        return self.volume_total * self.densite

    @property
    def surface_totale(self):
        "Surface externe totale approximative (m²)"
        surf_corps = 2 * (self.largeur + self.epaisseur) * self.longueur
        surf_tete = math.pi * self.diametre_tete * self.epaisseur
        surf_pied = math.pi * self.diametre_pied * self.epaisseur
        return surf_corps + surf_tete + surf_pied

    @property
    def moment_quadratique(self):
        "Moment quadratique de la section pour vérification RDM (m⁴)"
        # I = (b * h^3) / 12 pour rectangle (b = largeur, h = épaisseur)
        return (self.largeur * self.epaisseur ** 3) / 12

    def to_dict(self):
        return {
            "Longueur (mm)": round(self.longueur * 1000, 3),
            "Largeur (mm)": round(self.largeur * 1000, 3),
            "Épaisseur (mm)": round(self.epaisseur * 1000, 3),
            "Diamètre tête (mm)": round(self.diametre_tete * 1000, 3),
            "Diamètre pied (mm)": round(self.diametre_pied * 1000, 3),
            "Axe tête (mm)": round(self.axe_tete_diam * 1000, 3),
            "Axe pied (mm)": round(self.axe_pied_diam * 1000, 3),
            "Matière": self.matiere,
            "Densité (kg/m3)": self.densite,
            "État de surface": self.etat_surface,
            "Rugosité (Ra, µm)": self.rugosite,
            "Masse (kg)": round(self.masse, 5),
            "Volume total (cm3)": round(self.volume_total * 1e6, 3),
            "Surface totale (cm2)": round(self.surface_totale * 1e4, 3),
            "Moment quadratique (mm4)": round(self.moment_quadratique * 1e12, 2),
        }

    def __repr__(self):
        return (
            f"BielleStirling(L={self.longueur*1000:.2f} mm, "
            f"section={self.largeur*1000:.2f}x{self.epaisseur*1000:.2f} mm, "
            f"Tête={self.diametre_tete*1000:.2f} mm, Pied={self.diametre_pied*1000:.2f} mm, "
            f"{self.matiere}, Ra={self.rugosite} µm, {self.etat_surface})"
        )

# Exemple d’utilisation :
if __name__ == "__main__":
    bielle = BielleStirling(
        longueur_m=0.048,
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
    print(bielle)
    print("Paramètres CAO :", bielle.to_dict())
