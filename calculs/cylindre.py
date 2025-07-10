# calculs/cylindre.py
import math

class CylindreStirling:
    """
    Modélisation d’un cylindre de moteur Stirling pour CAO :
    - Zones chaude/froide paramétrables, géométrie, matière, masse, état de surface, visserie, RDM.
    """

    # Tableau ISO des diamètres de perçage pour taraudage (mm)
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
        diametre_m,
        course_m,
        epaisseur_m,
        matiere,
        densite_kg_m3,
        rugosite_um,
        etat_surface,
        Tc,
        Th,
        nb_vis,
        dim_vis_iso,
        entraxe_vis_pct,
        limite_rupture_MPa
    ):
        # Contrôles stricts : aucune valeur par défaut, tout doit être explicitement renseigné
        if any(x is None for x in [
            diametre_m, course_m, epaisseur_m, matiere, densite_kg_m3, rugosite_um,
            etat_surface, Tc, Th, nb_vis, dim_vis_iso, entraxe_vis_pct, limite_rupture_MPa
        ]):
            raise ValueError("Tous les paramètres sont obligatoires, aucun défaut n’est accepté.")

        if diametre_m <= 0 or course_m <= 0 or epaisseur_m <= 0:
            raise ValueError("Diamètre, course et épaisseur doivent être strictement positifs.")

        # Récupération diamètre perçage vis en mm
        diam_percage_mm = self.DIAM_PERCAGE_TARAUD_ISO.get(dim_vis_iso, 5.0)

        # Vérification que l’épaisseur est au moins égale au diamètre perçage vis (en m)
        epaisseur_min = diam_percage_mm / 1000.0  # Converti en mètres
        if epaisseur_m < epaisseur_min:
            print(f"Attention : épaisseur de paroi {epaisseur_m*1000:.1f} mm trop faible pour vis {dim_vis_iso} "
                  f"(minimum requis {epaisseur_min*1000:.1f} mm). Ajustement automatique.")
            epaisseur_m = epaisseur_min

        self.diametre = diametre_m
        self.course = course_m
        self.epaisseur = epaisseur_m
        self.matiere = matiere
        self.densite = densite_kg_m3
        self.rugosite = rugosite_um
        self.etat_surface = etat_surface
        self.Tc = Tc
        self.Th = Th
        # Visserie
        self.nb_vis = nb_vis
        self.dim_vis_iso = dim_vis_iso
        self.diam_percage_vis = diam_percage_mm / 1000.0  # m
        self.diam_taraudage_nominal = int(dim_vis_iso[1:]) / 1000.0 if dim_vis_iso.startswith("M") else 0.006
        self.entraxe_vis = (self.diametre / 2) * entraxe_vis_pct
        self.entraxe_vis_pct = entraxe_vis_pct
        self.limite_rupture_MPa = limite_rupture_MPa

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
        return math.pi * (self.rayon ** 2) * self.course

    @property
    def volume_metal(self):
        vi = self.volume_interne
        ve = math.pi * (self.rayon_ext ** 2) * self.course
        fond = math.pi * (self.rayon_ext ** 2) * self.epaisseur
        return max(ve - vi, 0) + fond

    @property
    def masse(self):
        return self.volume_metal * self.densite

    @property
    def surface_interne(self):
        return math.pi * self.diametre * self.course

    @property
    def surface_fond(self):
        return math.pi * (self.rayon ** 2)

    @property
    def surface_externe(self):
        return math.pi * self.diametre_ext * self.course

    @property
    def surface_totale_interne(self):
        return self.surface_interne + 2 * self.surface_fond

    @property
    def surface_totale_externe(self):
        sf = math.pi * (self.rayon_ext ** 2)
        return self.surface_externe + 2 * sf

    @property
    def perçage_vis(self):
        """Coordonnées (x, y) des centres de vis sur l'entraxe (mm)"""
        result = []
        r = self.entraxe_vis * 1000  # mm
        for i in range(self.nb_vis):
            a = 2 * math.pi * i / self.nb_vis
            x = r * math.cos(a)
            y = r * math.sin(a)
            result.append((round(x, 2), round(y, 2)))
        return result

    @property
    def section_anneau_autour_taraudage(self):
        """Section annulaire de paroi restante autour du trou taraudé (mm²)"""
        r_ext = self.rayon_ext * 1000  # mm
        r_trou = self.diam_percage_vis * 1000 / 2
        section = math.pi * (r_ext ** 2 - r_trou ** 2) - math.pi * (self.rayon ** 2)
        return max(section, 0)  # mm²

    @property
    def effort_max_admissible_par_taraudage(self):
        """Effort admissible par vis (cisaillement ou arrachement paroi) en N"""
        S = self.section_anneau_autour_taraudage / 1e6  # mm² -> m²
        # Limite en traction (N)
        return S * self.limite_rupture_MPa * 1e6  # (m²)*(Pa)

    @property
    def effort_total_visserie(self):
        """Effort total admissible par la visserie (N)"""
        return self.nb_vis * self.effort_max_admissible_par_taraudage

    @property
    def pression_maxi_admissible(self):
        """Pression admissible (Pa) sur la face avant avant rupture des taraudages (≈ sécurité)"""
        S_fond = self.surface_fond  # m²
        return self.effort_total_visserie / S_fond if S_fond else 0

    def zone_chaude(self, frac):
        if not (0 < frac <= 1):
            raise ValueError("Le paramètre frac doit être compris entre 0 exclu et 1 inclus.")
        lz = self.course * frac
        sz = math.pi * self.diametre * lz
        return lz, sz

    def zone_froide(self, frac):
        if not (0 < frac <= 1):
            raise ValueError("Le paramètre frac doit être compris entre 0 exclu et 1 inclus.")
        lz = self.course * frac
        sz = math.pi * self.diametre * lz
        return lz, sz

    def to_dict(self):
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
            "Visserie ISO": self.dim_vis_iso,
            "Nb vis": self.nb_vis,
            "Diam. perçage taraudage (mm)": round(self.diam_percage_vis * 1000, 2),
            "Rayon entraxe vis (mm)": round(self.entraxe_vis * 1000, 2),
            "Positions vis (mm)": self.perçage_vis,
            "Section paroi autour vis (mm2)": round(self.section_anneau_autour_taraudage, 2),
            "Effort max/vis (N)": int(self.effort_max_admissible_par_taraudage),
            "Effort total visserie (N)": int(self.effort_total_visserie),
            "Pression max admissible (bar)": round(self.pression_maxi_admissible / 1e5, 2),
        }

    def __repr__(self):
        return (
            f"CylindreStirling(D={self.diametre*1000:.2f} mm, C={self.course*1000:.2f} mm, "
            f"e={self.epaisseur*1000:.2f} mm, vis={self.nb_vis}x{self.dim_vis_iso}, "
            f"Rupture: {self.pression_maxi_admissible/1e5:.1f} bar, "
            f"{self.matiere}, Ra={self.rugosite} µm, {self.etat_surface})"
        )


# Exemple d’utilisation (tous les paramètres doivent venir d’un calcul préalable, aucune valeur par défaut)
if __name__ == "__main__":
    # Tous les paramètres doivent être passés explicitement !
    cyl = CylindreStirling(
        diametre_m=0.022,
        course_m=0.018,
        epaisseur_m=0.005,  # corrigé pour être compatible M6
        matiere="Acier inox 316L",
        densite_kg_m3=8000,
        rugosite_um=0.4,
        etat_surface="Rectifié miroir",
        Th=850,
        Tc=300,
        nb_vis=6,
        dim_vis_iso="M6",
        entraxe_vis_pct=0.85,
        limite_rupture_MPa=700
    )
    print(cyl)
    print("Paramètres CAO et RDM :", cyl.to_dict())
    chaud_len, chaud_surf = cyl.zone_chaude(frac=0.6)
    print(f"Zone chaude (60%) : longueur {chaud_len*1e3:.2f} mm, surface {chaud_surf*1e4:.2f} cm²")
