# calculs/displacer.py

import math

class DisplacerStirling:
    """
    Modélisation d’un displacer ("galette" séparatrice) pour moteur Stirling :
    - Géométrie, matière, densité, masse, surfaces, état de surface, etc.
    """

    def __init__(
        self,
        diametre_m,
        hauteur_m,
        epaisseur_fond_m=0.001,          # Épaisseur extrémité/plateaux (m), typique : 1mm
        matiere="Alliage léger",
        densite_kg_m3=2700,              # Par défaut : aluminium
        axe_diam_m=0.006,                # Diamètre axe central (6 mm par défaut)
        axe_longueur_m=None,             # Longueur axe, défaut=hauteur galette
        rugosite_um=1.6,                 # Ra (microns)
        etat_surface="Tournage fin"
    ):
        if diametre_m <= 0 or hauteur_m <= 0 or epaisseur_fond_m < 0:
            raise ValueError("Dimensions invalides")
        self.diametre = diametre_m
        self.hauteur = hauteur_m
        self.epaisseur_fond = epaisseur_fond_m
        self.matiere = matiere
        self.densite = densite_kg_m3
        self.axe_diam = axe_diam_m
        self.axe_longueur = axe_longueur_m if axe_longueur_m else hauteur_m
        self.rugosite = rugosite_um
        self.etat_surface = etat_surface

    @property
    def rayon(self):
        return self.diametre / 2

    @property
    def volume_displacer(self):
        """Volume apparent du displacer, sans axe (m³)"""
        return math.pi * (self.rayon ** 2) * self.hauteur

    @property
    def volume_axe(self):
        """Volume de l’axe (m³)"""
        r = self.axe_diam / 2
        return math.pi * (r ** 2) * self.axe_longueur

    @property
    def volume_total(self):
        """Volume total galette + axe (m³)"""
        return self.volume_displacer + self.volume_axe

    @property
    def masse(self):
        """Masse totale (kg)"""
        return self.volume_total * self.densite

    @property
    def surface_lat(self):
        """Surface latérale de la galette (m²)"""
        return math.pi * self.diametre * self.hauteur

    @property
    def surface_faces(self):
        """Surface totale des deux faces (m²)"""
        return 2 * math.pi * (self.rayon ** 2)

    @property
    def surface_totale(self):
        """Surface totale (latérale + 2 faces + axe, m²)"""
        axe_surf = math.pi * self.axe_diam * self.axe_longueur + 2 * math.pi * (self.axe_diam / 2) ** 2
        return self.surface_lat + self.surface_faces + axe_surf

    def to_dict(self):
        """Export complet des infos pour la CAO"""
        return {
            "Diamètre galette (mm)": round(self.diametre * 1000, 3),
            "Hauteur galette (mm)": round(self.hauteur * 1000, 3),
            "Épaisseur fonds (mm)": round(self.epaisseur_fond * 1000, 3),
            "Diamètre axe (mm)": round(self.axe_diam * 1000, 3),
            "Longueur axe (mm)": round(self.axe_longueur * 1000, 3),
            "Matière": self.matiere,
            "Densité (kg/m3)": self.densite,
            "Rugosité (Ra, µm)": self.rugosite,
            "État de surface": self.etat_surface,
            "Masse (kg)": round(self.masse, 5),
            "Volume total (cm3)": round(self.volume_total * 1e6, 3),
            "Surface totale (cm2)": round(self.surface_totale * 1e4, 3),
        }

    def __repr__(self):
        return (
            f"DisplacerStirling(D={self.diametre*1000:.2f} mm, H={self.hauteur*1000:.2f} mm, "
            f"axe Ø={self.axe_diam*1000:.2f} mm, {self.matiere}, {self.etat_surface}, Ra={self.rugosite} µm)"
        )

# Exemple d’utilisation
if __name__ == "__main__":
    galette = DisplacerStirling(
        diametre_m=0.021,
        hauteur_m=0.017,
        epaisseur_fond_m=0.001,
        matiere="Aluminium 6061",
        densite_kg_m3=2700,
        axe_diam_m=0.006,
        axe_longueur_m=0.025,
        rugosite_um=1.6,
        etat_surface="Tournage polissage"
    )
    print(galette)
    print("Paramètres CAO :", galette.to_dict())
