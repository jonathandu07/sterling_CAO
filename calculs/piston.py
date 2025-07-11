# calculs/piston.py
from calculs.cylindre import CylindreStirling
import math

class PistonStirling:
    """
    Modélisation d’un piston de moteur Stirling pour CAO :
    Généré à partir du cylindre, avec masse, volume, surfaces, rainures.
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

        # Dimensions des rainures selon la norme ISO 3601
        self.rainures = self._calculer_rainures()

    @classmethod
    def depuis_cylindre(cls, cylindre: CylindreStirling):
        diam = cylindre.diametre
        course = cylindre.course

        hauteur_piston = course * 0.9
        ep_fond = 0.003  # 3 mm
        ep_jupe = 0.002  # 2 mm
        hauteur_jupe = hauteur_piston - ep_fond
        nb_rainures = 2 if diam < 0.04 else 3

        axe_diam = diam * 0.4
        axe_longueur = diam * 0.8

        matiere = "AlSi12"
        densite = 2680
        rugosite = 0.8
        etat_surface = "Rectifié"

        return cls(
            diametre_m=diam,
            hauteur_m=hauteur_piston,
            epaisseur_fond_m=ep_fond,
            epaisseur_jupe_m=ep_jupe,
            hauteur_jupe_m=hauteur_jupe,
            matiere=matiere,
            densite_kg_m3=densite,
            rugosite_um=rugosite,
            etat_surface=etat_surface,
            nb_rainures=nb_rainures,
            axe_diam_m=axe_diam,
            axe_longueur_m=axe_longueur
        )

    def _calculer_rainures(self):
        """
        Renvoie une liste de rainures adaptées à ce piston.
        Chaque rainure contient (largeur, profondeur, position)
        """
        rainures = []
        # Largeur typique = 2 à 3 mm pour des pistons < 40 mm
        largeur = 0.0025 if self.diametre <= 0.04 else 0.003
        profondeur = largeur * 0.75
        espacement = (self.hauteur_jupe - self.nb_rainures * largeur) / (self.nb_rainures + 1)

        position = espacement
        for _ in range(self.nb_rainures):
            rainures.append({
                "largeur_m": largeur,
                "profondeur_m": profondeur,
                "position_depuis_bas_m": position
            })
            position += largeur + espacement
        return rainures

    @property
    def masse(self):
        return self.volume_total * self.densite

    @property
    def rayon(self):
        return self.diametre / 2

    @property
    def volume_externe(self):
        return math.pi * self.rayon**2 * self.hauteur

    @property
    def volume_interne(self):
        r_int = self.rayon - self.epaisseur_jupe
        return max(0, math.pi * r_int**2 * self.hauteur_jupe)

    @property
    def volume_fond(self):
        return math.pi * self.rayon**2 * self.epaisseur_fond

    @property
    def volume_axe(self):
        r = self.axe_diam / 2
        return math.pi * r**2 * self.axe_longueur

    @property
    def volume_total(self):
        return self.volume_externe - self.volume_interne + self.volume_axe

    @property
    def surface_totale(self):
        surf_lateral = math.pi * self.diametre * self.hauteur
        surf_faces = 2 * math.pi * self.rayon**2
        surf_axe = math.pi * self.axe_diam * self.axe_longueur + 2 * math.pi * (self.axe_diam / 2)**2
        return surf_lateral + surf_faces + surf_axe

    def to_dict(self):
        return {
            "Diamètre (mm)": round(self.diametre * 1000, 2),
            "Hauteur (mm)": round(self.hauteur * 1000, 2),
            "Épaisseur fond (mm)": round(self.epaisseur_fond * 1000, 2),
            "Épaisseur jupe (mm)": round(self.epaisseur_jupe * 1000, 2),
            "Hauteur jupe (mm)": round(self.hauteur_jupe * 1000, 2),
            "Matière": self.matiere,
            "Densité (kg/m3)": self.densite,
            "Rainures": [{
                "Largeur (mm)": round(r["largeur_m"] * 1000, 2),
                "Profondeur (mm)": round(r["profondeur_m"] * 1000, 2),
                "Position (mm)": round(r["position_depuis_bas_m"] * 1000, 2)
            } for r in self.rainures],
            "Masse (g)": round(self.masse * 1000, 2),
            "Volume (cm³)": round(self.volume_total * 1e6, 2),
            "Surface (cm²)": round(self.surface_totale * 1e4, 2),
        }

    def __repr__(self):
        return f"PistonStirling(D={self.diametre*1000:.2f}mm, H={self.hauteur*1000:.2f}mm, Rainures={self.nb_rainures})"
