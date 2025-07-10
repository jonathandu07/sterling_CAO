# calculs/axe_piston.py

import math

class AxePistonStirling:
    """
    Modélisation d’un axe de piston (arbre du piston) pour CAO :
    - Géométrie, volume, masse, matière, état de surface, propriétés mécaniques
    """

    def __init__(
        self,
        diametre_m,                  # Diamètre de l’axe (m)
        longueur_m,                  # Longueur totale (m)
        matiere="Acier trempé",
        densite_kg_m3=7850,
        rugosite_um=0.8,
        etat_surface="Rectifié"
    ):
        if diametre_m <= 0 or longueur_m <= 0:
            raise ValueError("Diamètre ou longueur d’axe non valides")
        self.diametre = diametre_m
        self.longueur = longueur_m
        self.matiere = matiere
        self.densite = densite_kg_m3
        self.rugosite = rugosite_um
        self.etat_surface = etat_surface

    @property
    def rayon(self):
        return self.diametre / 2

    @property
    def section(self):
        "Section droite (m²)"
        return math.pi * (self.rayon ** 2)

    @property
    def volume(self):
        "Volume total (m³)"
        return self.section * self.longueur

    @property
    def masse(self):
        "Masse totale (kg)"
        return self.volume * self.densite

    @property
    def surface_laterale(self):
        "Surface latérale de l’axe (m²)"
        return math.pi * self.diametre * self.longueur

    @property
    def moment_inertie(self):
        "Moment quadratique (m⁴), flexion"
        return (math.pi / 64) * self.diametre ** 4

    @property
    def module_resistance(self):
        "Module de résistance à la flexion (m³)"
        return self.moment_inertie / (self.diametre / 2)

    def to_dict(self):
        return {
            "Diamètre axe (mm)": round(self.diametre * 1000, 3),
            "Longueur axe (mm)": round(self.longueur * 1000, 3),
            "Matière": self.matiere,
            "Densité (kg/m3)": self.densite,
            "Rugosité (Ra, µm)": self.rugosite,
            "État de surface": self.etat_surface,
            "Masse (kg)": round(self.masse, 5),
            "Volume (cm3)": round(self.volume * 1e6, 3),
            "Surface latérale (cm2)": round(self.surface_laterale * 1e4, 3),
            "Section droite (mm2)": round(self.section * 1e6, 3),
            "Moment quadratique I (mm4)": round(self.moment_inertie * 1e12, 2),
            "Module de résistance W (mm3)": round(self.module_resistance * 1e9, 2),
        }

    def __repr__(self):
        return (
            f"AxePistonStirling(D={self.diametre*1000:.2f} mm, L={self.longueur*1000:.2f} mm, "
            f"{self.matiere}, Ra={self.rugosite} µm, {self.etat_surface})"
        )

# Exemple d’utilisation :
if __name__ == "__main__":
    axe = AxePistonStirling(
        diametre_m=0.008,     # 8 mm
        longueur_m=0.025,     # 25 mm
        matiere="Acier trempé 100Cr6",
        densite_kg_m3=7810,
        rugosite_um=0.6,
        etat_surface="Rectifié miroir"
    )
    print(axe)
    print("Paramètres CAO :", axe.to_dict())
