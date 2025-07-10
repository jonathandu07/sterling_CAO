# calculs/piston.py

import math

class PistonStirling:
    """
    Modélisation d’un piston de moteur Stirling pour CAO :
    - Géométrie complète, volume, masse, matière, état de surface, axe, rainures.
    """

    def __init__(
        self,
        diametre_m,
        hauteur_m,
        epaisseur_fond_m,
        epaisseur_jupe_m,
        hauteur_jupe_m,
        matiere,
        densite_kg_m3,
        rugosite_um,
        etat_surface,
        nb_rainures,
        axe_diam_m,
        axe_longueur_m
    ):
        # Tous les paramètres sont OBLIGATOIRES, aucun défaut accepté.
        params = [diametre_m, hauteur_m, epaisseur_fond_m, epaisseur_jupe_m, hauteur_jupe_m,
                  matiere, densite_kg_m3, rugosite_um, etat_surface, nb_rainures, axe_diam_m, axe_longueur_m]
        if any(x is None for x in params):
            raise ValueError("Tous les paramètres doivent être explicitement renseignés (aucun défaut accepté).")
        if diametre_m <= 0 or hauteur_m <= 0 or epaisseur_fond_m <= 0 or epaisseur_jupe_m <= 0 or hauteur_jupe_m <= 0 or axe_diam_m <= 0 or axe_longueur_m <= 0:
            raise ValueError("Dimensions invalides (doivent être > 0)")
        self.diametre = diametre_m
        self.hauteur = hauteur_m
        self.epaisseur_fond = epaisseur_fond_m
        self.epaisseur_jupe = epaisseur_jupe_m
        self.hauteur_jupe = hauteur_jupe_m
        self.matiere = matiere
        self.densite = densite_kg_m3
        self.rugosite = rugosite_um
        self.etat_surface = etat_surface
        self.nb_rainures = nb_rainures
        self.axe_diam = axe_diam_m
        self.axe_longueur = axe_longueur_m

    @property
    def rayon(self):
        return self.diametre / 2

    @property
    def volume_externe(self):
        """Volume externe (m³), piston considéré comme un cylindre plein"""
        return math.pi * (self.rayon ** 2) * self.hauteur

    @property
    def volume_interne(self):
        """Volume creusé sous le piston, hors jupe et fond"""
        r_int = self.rayon - self.epaisseur_jupe
        if r_int < 0:
            return 0
        return math.pi * (r_int ** 2) * self.hauteur_jupe

    @property
    def volume_fond(self):
        """Volume du fond du piston (m³)"""
        return math.pi * (self.rayon ** 2) * self.epaisseur_fond

    @property
    def volume_axe(self):
        """Volume de l’axe (m³)"""
        r_axe = self.axe_diam / 2
        return math.pi * (r_axe ** 2) * self.axe_longueur

    @property
    def volume_total(self):
        """Volume total (jupe + fond + axe, m³)"""
        # Piston = cylindre plein - vide intérieur + axe
        return self.volume_externe - self.volume_interne + self.volume_axe

    @property
    def masse(self):
        """Masse totale (kg)"""
        return self.volume_total * self.densite

    @property
    def surface_laterale(self):
        """Surface latérale externe (m²), utile pour friction et échanges thermiques"""
        return math.pi * self.diametre * self.hauteur

    @property
    def surface_faces(self):
        """Surface des deux faces du piston (m²)"""
        return 2 * math.pi * (self.rayon ** 2)

    @property
    def surface_totale(self):
        """Surface totale (latérale + 2 faces + axe, m²)"""
        axe_surf = math.pi * self.axe_diam * self.axe_longueur + 2 * math.pi * (self.axe_diam / 2) ** 2
        return self.surface_laterale + self.surface_faces + axe_surf

    @property
    def longueur_axe(self):
        return self.axe_longueur

    def to_dict(self):
        """Export complet des paramètres pour CAO / SolidWorks"""
        return {
            "Diamètre piston (mm)": round(self.diametre * 1000, 3),
            "Hauteur piston (mm)": round(self.hauteur * 1000, 3),
            "Épaisseur fond (mm)": round(self.epaisseur_fond * 1000, 3),
            "Épaisseur jupe (mm)": round(self.epaisseur_jupe * 1000, 3),
            "Hauteur jupe (mm)": round(self.hauteur_jupe * 1000, 3),
            "Matière": self.matiere,
            "Densité (kg/m3)": self.densite,
            "Rugosité (Ra, µm)": self.rugosite,
            "État de surface": self.etat_surface,
            "Nb rainures": self.nb_rainures,
            "Diamètre axe (mm)": round(self.axe_diam * 1000, 3),
            "Longueur axe (mm)": round(self.axe_longueur * 1000, 3),
            "Masse (kg)": round(self.masse, 5),
            "Volume total (cm3)": round(self.volume_total * 1e6, 3),
            "Surface totale (cm2)": round(self.surface_totale * 1e4, 3),
        }

    def __repr__(self):
        return (
            f"PistonStirling(D={self.diametre*1000:.2f} mm, H={self.hauteur*1000:.2f} mm, "
            f"fond={self.epaisseur_fond*1000:.2f} mm, jupe={self.epaisseur_jupe*1000:.2f} mm, "
            f"{self.matiere}, Ra={self.rugosite} µm, {self.etat_surface})"
        )

# Exemple d’utilisation (aucun paramètre par défaut, tout doit être explicitement donné)
if __name__ == "__main__":
    piston = PistonStirling(
        diametre_m=0.021,
        hauteur_m=0.018,
        epaisseur_fond_m=0.003,
        epaisseur_jupe_m=0.002,
        hauteur_jupe_m=0.015,
        matiere="AlSi12",
        densite_kg_m3=2680,
        rugosite_um=0.5,
        etat_surface="Microbillage + rectif",
        nb_rainures=2,
        axe_diam_m=0.008,
        axe_longueur_m=0.025
    )
    print(piston)
    print("Paramètres CAO :", piston.to_dict())
