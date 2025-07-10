# calculs/couvercle_cylindre.py

import math

class CouvercleCylindreStirling:
    """
    Modélisation d’un couvercle de cylindre Stirling :
    - Entrées d’air, brûleur
    - Taraudage pour vis de fixation ISO (M4 à M16…)
    - Toutes options géométriques et masses
    """

    # Tableau ISO des diamètres de perçage pour taraudage (pas gros standard, mm)
    DIAM_PERCAGE_TARAUD_ISO = {
        "M4": 3.3,
        "M5": 4.2,
        "M6": 5.0,
        "M8": 6.8,
        "M10": 8.5,
        "M12": 10.2,
        "M16": 14.0,
    }

    def __init__(
        self,
        diametre_m,                         # Diamètre du cylindre/couvercle (m)
        epaisseur_m=0.005,                  # Épaisseur couvercle (m)
        matiere="Acier inox",
        densite_kg_m3=7900,
        rugosite_um=1.2,
        etat_surface="Rectifié fin",
        type_couvercle="plat",              # "plat" ou "bombé"
        # Entrées d’air principales
        diam_entrée_air_m=0.008,
        nb_entree_air=1,
        # Entrée brûleur
        diam_entrée_bruleur_m=0.012,
        nb_entree_bruleur=1,
        distance_bruleur_centre_m=None,
        # Taraudages de fixation ISO
        nb_vis=4,
        dim_vis_iso="M6",
        entraxe_vis_pct=0.85   # % du rayon utilisé pour l'entraxe (0.8~0.9)
    ):
        if diametre_m <= 0 or epaisseur_m <= 0:
            raise ValueError("Dimensions invalides")
        self.diametre = diametre_m
        self.epaisseur = epaisseur_m
        self.matiere = matiere
        self.densite = densite_kg_m3
        self.rugosite = rugosite_um
        self.etat_surface = etat_surface
        self.type_couvercle = type_couvercle
        self.diam_entrée_air = diam_entrée_air_m
        self.nb_entree_air = nb_entree_air
        self.diam_entrée_bruleur = diam_entrée_bruleur_m
        self.nb_entree_bruleur = nb_entree_bruleur
        self.distance_bruleur_centre = distance_bruleur_centre_m if distance_bruleur_centre_m is not None else 0.0
        # Taraudage ISO
        self.nb_vis = nb_vis
        self.dim_vis_iso = dim_vis_iso
        self.diam_percage_vis = self.DIAM_PERCAGE_TARAUD_ISO.get(dim_vis_iso, 5.0) / 1000.0  # en mètre
        self.diam_taraudage_nominal = int(dim_vis_iso[1:]) / 1000.0 if dim_vis_iso.startswith("M") else 0.006 # mm -> m
        self.entraxe_vis = (self.diametre / 2) * entraxe_vis_pct  # rayon d’entraxe (m)
        self.entraxe_vis_pct = entraxe_vis_pct

    @property
    def rayon(self):
        return self.diametre / 2

    @property
    def surface_totale(self):
        return math.pi * (self.rayon ** 2)

    @property
    def volume(self):
        if self.type_couvercle == "plat":
            return self.surface_totale * self.epaisseur
        elif self.type_couvercle == "bombé":
            h = self.epaisseur
            r = self.rayon
            calotte = (math.pi * h ** 2 * (3 * r - h)) / 3
            return self.surface_totale * h + calotte
        else:
            raise ValueError("Type de couvercle inconnu")

    @property
    def volume_percages(self):
        # Entrées d’air
        v_entree_air = self.nb_entree_air * math.pi * (self.diam_entrée_air / 2) ** 2 * self.epaisseur
        v_entree_bruleur = self.nb_entree_bruleur * math.pi * (self.diam_entrée_bruleur / 2) ** 2 * self.epaisseur
        # Trous pour taraudage (diamètre de perçage ISO)
        v_percage_vis = self.nb_vis * math.pi * (self.diam_percage_vis / 2) ** 2 * self.epaisseur
        return v_entree_air + v_entree_bruleur + v_percage_vis

    @property
    def volume_net(self):
        v = self.volume - self.volume_percages
        return max(v, 0)

    @property
    def masse(self):
        return self.volume_net * self.densite

    @property
    def profondeur_taraudage(self):
        """
        Profondeur de taraudage recommandée : 1x à 1.5x diamètre nominal pour l'acier.
        (ici, min = 1x diam)
        """
        return round(self.diam_taraudage_nominal * 1000, 2)  # en mm

    @property
    def perçage_vis(self):
        """Renvoie (x, y) des centres de perçages sur le cercle d’entraxe (mm)"""
        result = []
        angle0 = 0  # Peut ajouter un décalage angulaire si besoin
        r = self.entraxe_vis * 1000  # mm
        for i in range(self.nb_vis):
            a = angle0 + 2 * math.pi * i / self.nb_vis
            x = r * math.cos(a)
            y = r * math.sin(a)
            result.append((round(x, 2), round(y, 2)))
        return result

    def to_dict(self):
        return {
            "Diamètre (mm)": round(self.diametre * 1000, 3),
            "Épaisseur (mm)": round(self.epaisseur * 1000, 3),
            "Type": self.type_couvercle,
            "Matière": self.matiere,
            "Densité (kg/m3)": self.densite,
            "Rugosité (Ra, µm)": self.rugosite,
            "État de surface": self.etat_surface,
            "Entrée air (mm)": round(self.diam_entrée_air * 1000, 2),
            "Nb entrées air": self.nb_entree_air,
            "Entrée brûleur (mm)": round(self.diam_entrée_bruleur * 1000, 2),
            "Nb entrées brûleur": self.nb_entree_bruleur,
            "Dist. brûleur au centre (mm)": round(self.distance_bruleur_centre * 1000, 2),
            "Vis fixation ISO": self.dim_vis_iso,
            "Nb vis": self.nb_vis,
            "Diam. perçage taraudage (mm)": round(self.diam_percage_vis * 1000, 2),
            "Profondeur taraudage min. (mm)": self.profondeur_taraudage,
            "Rayon entraxe vis (mm)": round(self.entraxe_vis * 1000, 2),
            "Positions vis (mm)": self.perçage_vis,
            "Masse (kg)": round(self.masse, 5),
            "Volume net (cm3)": round(self.volume_net * 1e6, 3),
            "Surface (cm2)": round(self.surface_totale * 1e4, 3),
        }

    def __repr__(self):
        return (
            f"CouvercleCylindreStirling(D={self.diametre*1000:.2f} mm, e={self.epaisseur*1000:.2f} mm, "
            f"{self.type_couvercle}, air={self.nb_entree_air}x{self.diam_entrée_air*1000:.1f} mm, "
            f"brûleur={self.nb_entree_bruleur}x{self.diam_entrée_bruleur*1000:.1f} mm, "
            f"vis={self.nb_vis}x{self.dim_vis_iso}, "
            f"{self.matiere}, Ra={self.rugosite} µm)"
        )

# Exemple d’utilisation :
if __name__ == "__main__":
    couvercle = CouvercleCylindreStirling(
        diametre_m=0.022,
        epaisseur_m=0.005,
        matiere="Inox 310S",
        densite_kg_m3=7950,
        rugosite_um=0.6,
        etat_surface="Rectifié miroir",
        type_couvercle="plat",
        diam_entrée_air_m=0.008,
        nb_entree_air=1,
        diam_entrée_bruleur_m=0.012,
        nb_entree_bruleur=1,
        distance_bruleur_centre_m=0.0,
        nb_vis=6,
        dim_vis_iso="M6",
        entraxe_vis_pct=0.85
    )
    print(couvercle)
    print("Paramètres CAO :", couvercle.to_dict())
