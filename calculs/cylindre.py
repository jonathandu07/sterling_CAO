# calculs/cylindre.py

import math

class CylindreStirling:
    """
    Modélisation d’un cylindre de moteur Stirling pour CAO :
    - Zones chaude et froide paramétrables
    - Géométrie, volume, surface, épaisseur, matière, masse, état de surface, etc.
    """

    def __init__(
        self,
        diametre_m,
        course_m,
        epaisseur_m=0.002,           # Épaisseur paroi (m), ex: 2mm
        matiere="Acier",
        densite_kg_m3=7850,          # Densité acier (par défaut)
        rugosite_um=0.8,             # Ra (microns)
        etat_surface="Usinage fin",  # Description usuelle
        Tc=300,
        Th=850,
    ):
        if diametre_m <= 0 or course_m <= 0 or epaisseur_m < 0:
            raise ValueError("Diamètre, course ou épaisseur non valides (doivent être > 0).")
        self.diametre = diametre_m
        self.course = course_m
        self.epaisseur = epaisseur_m
        self.matiere = matiere
        self.densite = densite_kg_m3 or 7850
        self.rugosite = rugosite_um or 0.8
        self.etat_surface = etat_surface or "Usinage fin"
        self.Tc = Tc
        self.Th = Th

    @property
    def rayon(self):
        return self.diametre / 2

    @property
    def rayon_ext(self):
        return self.rayon + self.epaisseur

    @property
    def diametre_ext(self):
        return self.diametre + 2 * self.epaisseur

    @property
    def volume_interne(self):
        "Volume total balayé par le piston (m³)"
        return math.pi * (self.rayon ** 2) * self.course

    @property
    def volume_metal(self):
        "Volume de métal (m³), cylindre à fond plat"
        vi = self.volume_interne
        ve = math.pi * (self.rayon_ext ** 2) * self.course
        # On rajoute le fond (épaisseur) :
        fond = math.pi * (self.rayon_ext ** 2) * self.epaisseur
        return max(ve - vi, 0) + fond

    @property
    def masse(self):
        "Masse du cylindre (kg), si densité renseignée"
        return self.volume_metal * self.densite

    @property
    def surface_interne(self):
        "Surface interne latérale (m²)"
        return math.pi * self.diametre * self.course

    @property
    def surface_fond(self):
        "Surface interne d'un fond (m²)"
        return math.pi * (self.rayon ** 2)

    @property
    def surface_externe(self):
        "Surface externe latérale (m²)"
        return math.pi * self.diametre_ext * self.course

    @property
    def surface_totale_interne(self):
        "Surface totale interne (latérale + 2 fonds, m²)"
        return self.surface_interne + 2 * self.surface_fond

    @property
    def surface_totale_externe(self):
        "Surface totale externe (latérale + 2 fonds, m²)"
        sf = math.pi * (self.rayon_ext ** 2)
        return self.surface_externe + 2 * sf

    def zone_chaude(self, frac=0.5):
        """
        Retourne (longueur, surface latérale) de la zone chaude.
        frac : proportion (0..1) de la course affectée à la zone chaude
        """
        lz = self.course * frac
        sz = math.pi * self.diametre * lz
        return lz, sz

    def zone_froide(self, frac=0.5):
        """
        Retourne (longueur, surface latérale) de la zone froide.
        """
        lz = self.course * frac
        sz = math.pi * self.diametre * lz
        return lz, sz

    def to_dict(self):
        "Export complet des paramètres pour CAO / SolidWorks"
        return {
            "Diamètre interne (mm)": round(self.diametre * 1000, 3),
            "Diamètre externe (mm)": round(self.diametre_ext * 1000, 3),
            "Course (mm)": round(self.course * 1000, 3),
            "Épaisseur paroi (mm)": round(self.epaisseur * 1000, 3),
            "Matière": self.matiere,
            "Densité (kg/m3)": self.densite,
            "Rugosité (Ra, µm)": self.rugosite,
            "État de surface": self.etat_surface,
            "Masse (kg)": round(self.masse, 5),
            "Volume interne (cm3)": round(self.volume_interne * 1e6, 3),
            "Volume métal (cm3)": round(self.volume_metal * 1e6, 3),
            "Surface interne totale (cm2)": round(self.surface_totale_interne * 1e4, 3),
            "Surface externe totale (cm2)": round(self.surface_totale_externe * 1e4, 3),
        }

    def __repr__(self):
        return (
            f"CylindreStirling(D={self.diametre*1000:.2f} mm, C={self.course*1000:.2f} mm, "
            f"e={self.epaisseur*1000:.2f} mm, Th={self.Th} K, Tc={self.Tc} K, "
            f"{self.matiere}, Ra={self.rugosite} µm, {self.etat_surface})"
        )

# Exemple d’utilisation :
if __name__ == "__main__":
    cyl = CylindreStirling(
        diametre_m=0.022,
        course_m=0.018,
        epaisseur_m=0.002,
        matiere="Acier inox 316L",
        densite_kg_m3=8000,
        rugosite_um=0.4,
        etat_surface="Rectifié miroir",
        Th=850,
        Tc=300
    )
    print(cyl)
    print("Paramètres CAO :", cyl.to_dict())
    chaud_len, chaud_surf = cyl.zone_chaude(frac=0.6)
    print(f"Zone chaude (60%) : longueur {chaud_len*1e3:.2f} mm, surface {chaud_surf*1e4:.2f} cm²")
